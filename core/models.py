from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=20, verbose_name='Кличка')
    age = models.IntegerField(verbose_name='Возраст')
    image = models.ImageField(verbose_name='Фото', blank=True, null=True)


    class Meta:
        verbose_name = 'кличка'
        verbose_name_plural = 'клички'
# Create your models here.
