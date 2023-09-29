from django.db import transaction
from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total = serializers.SerializerMethodField(method_name='item_total')

    class Meta:
        model = CartItems
        fields = ("id", "cart", "product", "quantity", 'total')

    def item_total(self, cart=CartItems):
        return cart.quantity * cart.product.product_price


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = CartItemSerializer(many=True, read_only=True)
    absolute_total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "absolute_total")

    def main_total(self,  allcart=Cart):
        items = allcart.items.all()
        total = sum([item.quantity * item.product.product_price for item in items])
        return total


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Нет ассоциации товара с данным ID")
        return value

    def save(self, *args, **kwargs):
        cart_id = self.context["cart_id"]
        user = self.context["user"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = CartItems.objects.get(product_id=product_id, user=user, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem

        except:
            self.instance = CartItems.objects.create(cart_id=cart_id, user=user, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItems
        fields = ("id", "product_id", "quantity")


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ("quantity",)


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id=user_id, pending_status='О')
            cart_items = CartItems.objects.filter(cart_id=cart_id)
            if cart_items.exists():
                order_items = [
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity)
                    for item in cart_items
                ]
                OrderItem.objects.bulk_create(order_items)
                Cart.objects.filter(id=cart_id).delete()
            else:
                raise serializers.ValidationError("Ваша корзина пустая.")


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "created", "pending_status", "owner", "items")
