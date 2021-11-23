from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db.models import QuerySet

from apps.main.models import Ad, Subscription
from apps.main.schemas import AdSchema, UserSchema


def get_subsription_users() -> QuerySet[User]:
    """Возвращает пользователей, подписанных на все подписки."""
    qs = User.objects.none()
    for sub in Subscription.objects.all():
        qs |= sub.user.all()
    qs = qs.distinct()
    return qs


def get_last_weeks_ads() -> QuerySet[Ad]:
    """Возвращает объявления за последнюю неделю."""
    return Ad.objects.filter(creation_date__gte=datetime.now() - timedelta(days=7))


def get_digest(serialize=True) -> tuple[QuerySet[User], QuerySet[Ad]] | tuple[UserSchema | list, AdSchema]:
    """Возвращает пользователей и объявления, необходимых для дайджеста"""
    users = get_subsription_users()
    ads = get_last_weeks_ads()
    if not serialize:
        return users, ads
    serialized_users = UserSchema.from_django(users, many=True)
    serialized_ads = AdSchema.from_django(ads, many=True)
    return serialized_users, serialized_ads
