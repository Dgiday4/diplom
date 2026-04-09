from django.db.models.signals import post_save
from django.dispatch import receiver
from webpush import send_user_notification
from core.models import DogComment


@receiver(post_save, sender=DogComment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        owner = instance.dog.profile.user  # через профиль к пользователю
        author = instance.author

        if owner == author:
            return

        payload = {
            "head": f"Новый комментарий от {author.username}",
            "body": f"К собаке «{instance.dog.name}»: {instance.text[:100]}",
            "icon": "https://via.placeholder.com/64/4a90e2/ffffff?text=🐕",
            "url": f"/dog/{instance.dog.id}/",
        }

        try:
            send_user_notification(user=owner, payload=payload, ttl=1000)
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")