from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from apps.main.models import Ad, Seller, Subscription


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
    seller = Seller.objects.create(user=user)
    seller.save()


@receiver(post_save, sender=Ad)
def send_email_to_subscribers(**kwargs):
    """Отправка email всем подписчикам о новом объявлении."""
    instance = kwargs.get('instance')
    subscriptions = Subscription.objects.all()
    users = set()
    [users.update(sub.user.iterator()) for sub in subscriptions]
    subject = f"New Ad {instance.title}"
    site_url = Site.objects.get_current().domain
    body = render_to_string('account/email/email_new_ad.html', {
        'ad_url': instance.url,
        'ad_title': instance.title,
        'site_url': site_url,
    })
    emails = (user.email for user in users if user.email)
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=f"noreply@{site_url}",
        to=emails
    )
    msg.content_subtype = "html"
    msg.send()
