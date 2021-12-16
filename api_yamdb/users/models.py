from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    """ Клас определяющий роли пользователей. ПО ТЗ 4 роли. Суперпользователя
будем вынимать из БД. """

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    """Расширяем модель полями биография и роль"""
    email = models.EmailField(blank=False, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.TextField(
        'Роль',
        max_length=24,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
