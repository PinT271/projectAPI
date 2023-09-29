from rest_framework import viewsets, mixins
from rest_framework.mixins import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .permissions import IsAdminOrReadOnly, IsOwner, IsAuthenticatedNotAdmin
from .serializers import *


# Отвечает за вывод списка товаров для всех пользователей, а админу разрешает добавлять, изменять и удалять товары
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)


# Отвечает за просмотр корзины владельцем, и позволяет создавать другие корзины для конкретного пользователя
class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticatedNotAdmin, IsOwner)


# Отвечает за представление товаров в корзине, а также позволяет добавлять, изменять и удалять товары
class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedNotAdmin, IsOwner)

    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return CartItems.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"], 'user': self.request.user}


# Отвечает за заказы и доступен только клиентам, позволяет создавать и просматривать заказы.
# Для владельца заказов будут выводиться все его заказы, в другом случае - ничего.
class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    permission_classes = (IsAuthenticatedNotAdmin,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer

        return OrderSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}
