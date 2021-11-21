from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db.models import QuerySet

from apps.main.models import Ad, Subscription


def get_subsription_users() -> set[User]:
    """Возвращает пользователей, подписанных на все подписки."""
    users = set()
    [users.update(sub.user.iterator()) for sub in Subscription.objects.all()]
    return users


def get_last_weeks_ads() -> QuerySet[Ad]:
    """Возвращает объявления за последнюю неделю."""
    return Ad.objects.filter(creation_date__gte=datetime.now() - timedelta(days=7))


def get_digest() -> tuple[set[User], QuerySet[Ad]]:
    """Возвращает пользователей и объявления, необходимых для дайджеста"""
    return get_subsription_users(), get_last_weeks_ads()
