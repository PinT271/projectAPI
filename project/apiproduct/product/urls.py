from django.urls import path, include
from rest_framework_nested import routers
from .views import *

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet)
router.register(r"carts", CartViewSet)
router.register(r"orders", OrderViewSet, basename="orders")

cart_router = routers.NestedSimpleRouter(router, "carts", lookup="cart")
cart_router.register(r"items-cart", CartItemViewSet, basename="cart-items")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
]