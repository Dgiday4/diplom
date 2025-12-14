from django.db import models
from users.models import Profile


class Dog(models.Model):
    name = models.CharField(max_length=20, verbose_name='Кличка')
    age = models.IntegerField(verbose_name='Возраст')
    image = models.ImageField(verbose_name='Фото', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='профиль пользователя')



    class Meta:
        verbose_name = 'кличка'
        verbose_name_plural = 'клички'
# Create your models here.
