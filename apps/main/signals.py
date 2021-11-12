from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    """Добавление нового пользователя в группу 'common users'."""
    if created:
        instance.groups.add(Group.objects.get(name='common users'))
