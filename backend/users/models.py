from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (USER, 'user'),
    )
    email = models.EmailField(
        verbose_name='Эл. Почта',
        unique=True,
        max_length=254,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=9,
    )

    class Meta:
        ordering = ('role', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.role == self.ADMIN

    def __str__(self):
        return self.username


class Follow(models.Model):
    ''' user - кто подписывается, following - на кого'''
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.following.username} подписан на {self.user.username}'
