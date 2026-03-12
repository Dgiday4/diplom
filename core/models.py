from django.db import models
from users.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class Dog(models.Model):
    name = models.CharField(max_length=20, verbose_name='Кличка')
    age = models.IntegerField(verbose_name='Возраст')
    image = models.ImageField(verbose_name='Фото', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='профиль пользователя')
    breed = models.CharField(max_length=100, verbose_name='Порода', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    health_status = models.CharField(max_length=50, verbose_name='Статус здоровья', default='Здоров', blank=True)



    class Meta:
        verbose_name = 'собака'
        verbose_name_plural = 'собаки'
# Create your models here.
class DogComment(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='comments', verbose_name='Собака')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dog_comments', verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Комментарий к собаке'
        verbose_name_plural = 'Комментарии к собакам'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}..."