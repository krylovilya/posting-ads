from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from apps.main.services.digest import get_digest


def send_email_to_subscribers():
    """Отправляет дайджест всем подписчикам."""
    digest = get_digest()
    if not digest:
        return
    users, ads = digest
    site_url = Site.objects.get_current().domain
    subject = "Hi! Check out our weekly digest"
    body = render_to_string('account/email/email_digest.html', {
        'site_url': site_url,
        'ads': ads,
        'ad_count': ads.count(),
    })
    emails = (user.email for user in users)
    msg = EmailMessage(subject, body, f"noreply@{site_url}", emails)
    msg.content_subtype = "html"
    msg.send()


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(
            send_email_to_subscribers,
            trigger=CronTrigger(day_of_week="mon"),
            replace_existing=True,
        )

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
