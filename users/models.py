from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=255, verbose_name='имя', blank=True)
    last_name = models.CharField(max_length=255, verbose_name='фамилия', blank=True)

    def __str__(self):
        return f"{self.user} {self.first_name}"


    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'

