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


class Friends(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends_with', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
        verbose_name = 'друг'
        verbose_name_plural = 'друзья'

    def __str__(self):
        return f"{self.user} дружит с {self.friend}"

    @classmethod
    def add_friend(cls, user, friend):
        if user == friend:
            return None, "Нельзя добавить в друзья самого себя"

        # Проверяем, не друзья ли уже
        if cls.objects.filter(user=user, friend=friend).exists():
            return None, "Уже друзья"

        # Создаем связь
        friendship = cls.objects.create(user=user, friend=friend)

        return friendship, "Добавлен в друзья"

    @classmethod
    def remove_friend(cls, user, friend):
        deleted_count, _ = cls.objects.filter(
            user=user,
            friend=friend
        ).delete()

        return deleted_count > 0, "Удален из друзей" if deleted_count > 0 else "Не был другом"

    @classmethod
    def get_friends(cls, user):
        return User.objects.filter(
            id__in=cls.objects.filter(user=user).values_list('friend', flat=True)
        )

    @classmethod
    def are_friends(cls, user1, user2):
        return cls.objects.filter(user=user1, friend=user2).exists()

    @classmethod
    def get_friends_count(cls, user):
        return cls.objects.filter(user=user).count()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )

    content = models.TextField(
        max_length=1000,
        verbose_name='Текст поста',
        blank=True
    )

    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True,
        verbose_name='Лайки'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']  #чтобы были новые сначала

    def __str__(self):
        return f"Пост от {self.author.username} - {self.created_at.strftime('%d.%m.%Y')}"

    def total_likes(self):
        #сумма лайков
        return self.likes.count()

    def is_liked_by(self, user):
        #проверка лайкнул ли пользователь пост
        return self.likes.filter(id=user.id).exists()


class Comment(models.Model):
    #комментарий к посту

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    text = models.TextField(
        max_length=500,
        verbose_name='Текст комментария'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f"Комментарий от {self.author.username}"