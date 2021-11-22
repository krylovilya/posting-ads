from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.main.services.digest import get_subsription_users
from config.celery import app


@app.task()
def send_email_to_subscribers_task(ad: dict[str, str]):
    """Celery task. Отправка email всем подписчикам о новом объявлении."""
    users = get_subsription_users()
    subject = f"New Ad {ad['ad_title']}"
    site_url = Site.objects.get_current().domain
    body = render_to_string('account/email/email_new_ad.html', ad | {'site_url': site_url})
    emails = (user.email for user in users if user.email)
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=f"noreply@{site_url}",
        to=emails
    )
    msg.content_subtype = "html"
    msg.send()
