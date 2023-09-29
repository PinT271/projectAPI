from django.db import models
from django.contrib.auth.models import AbstractUser


class ProductUser(AbstractUser):
    username = models.CharField(
        verbose_name="ФИО",
        max_length=120,
        help_text="Обязательное поле. Для правильного заполнения введите ФИО",
        error_messages={
            "error": "Пользователь с таким ФИО уже существует!"
        },
    )
    email = models.EmailField(verbose_name="Электронная почта", unique=True)

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
