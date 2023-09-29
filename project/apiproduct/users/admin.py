from django.contrib import admin
from .models import ProductUser


@admin.register(ProductUser)
class ProductUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
