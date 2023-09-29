from django.core.validators import MinValueValidator
from django.db import models
from users.models import ProductUser
import uuid


class Product(models.Model):
    product_name = models.CharField(verbose_name='Название товара', max_length=255)
    product_desc = models.TextField(verbose_name='Описание товара')
    product_price = models.PositiveIntegerField(verbose_name='Цена товара')
    product_category = models.ForeignKey('ProductCategory', verbose_name='Категория товара', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.product_name}, {self.product_category}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductCategory(models.Model):
    name = models.CharField('Название категории', max_length=100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(ProductUser, verbose_name="Пользователь корзины", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, verbose_name="Используемая корзина", on_delete=models.CASCADE, related_name="items")
    user = models.ForeignKey(ProductUser, verbose_name="Пользователь товара в корзине", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name="Товар в корзине", on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество товара в корзине", default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.product}, {self.quantity}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Order(models.Model):

    PAYMENT_STATUS_CHOISE =[
        ("О", "Оплачен"),
        ("З", "Завершен"),
        ("П", "Провален"),
    ]

    created = models.DateTimeField(verbose_name="Дата и время оформления заказа", auto_now_add=True)
    pending_status = models.CharField(verbose_name="Статус заказа", max_length=50, choices=PAYMENT_STATUS_CHOISE)
    owner = models.ForeignKey(ProductUser, on_delete=models.PROTECT, verbose_name="Владелец заказа")

    def __str__(self):
        return f'{self.pending_status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name="Заказ", related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество", default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.product.product_name}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
