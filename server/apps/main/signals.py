from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.main.models import Ad, Seller
from apps.main.tasks import send_email_to_subscribers_task


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    """Добавление нового пользователя в группу 'common users'."""
    if created:
        instance.groups.add(Group.objects.get(name='common users'))


@receiver(post_save, sender=User)
def connect_user_to_seller(**kwargs):
    """Проверка, что Продавец создан для пользователя."""
    if not kwargs.get('created', True):
        return
    user = kwargs.get('instance')
    Seller.objects.create(user=user)


@receiver(post_save, sender=Ad)
def send_email_to_subscribers(**kwargs):
    """Отправка email всем подписчикам о новом объявлении."""
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        send_email_to_subscribers_task.delay({
            'ad_title': instance.title,
            'ad_url': instance.url,
        })
