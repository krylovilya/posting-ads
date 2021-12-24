from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from twilio.rest import Client

from apps.main.services.digest import get_digest, get_subsription_users
from config.celery import app


@app.task()
def send_email_to_subscribers_task(ad: dict[str, str]):
    """Celery task. Отправка email всем подписчикам о новом объявлении."""
    users = get_subsription_users()
    subject = f"New Ad {ad['ad_title']}"
    site_url = Site.objects.get_current().domain
    body = render_to_string('account/email/email_new_ad.html', ad | {'site_url': site_url})
    emails = [user.email for user in users if user.email]
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=f"noreply@{site_url}",
        to=emails
    )
    msg.content_subtype = "html"
    msg.send()


@app.task()
def send_digest_task():
    """Celery task. Отправляет дайджест всем подписчикам."""
    digest = get_digest()
    if not digest:
        return
    users, ads = digest
    site_url = Site.objects.get_current().domain
    subject = "Hi! Check out our weekly digest"
    body = render_to_string('account/email/email_digest.html', {
        'site_url': site_url,
        'ads': ads[:5],
        'ad_count': len(ads),
    })
    emails = (user.email for user in users if user.email)
    msg = EmailMessage(subject, body, f"noreply@{site_url}", emails)
    msg.content_subtype = "html"
    msg.send()


@app.task()
def send_confirmation_code_by_sms(phone: str, confirmation_code: int):
    """Celery task. Отправляет смс с кодом"""
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=str(confirmation_code),
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
