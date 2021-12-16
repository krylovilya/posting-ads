import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

import factory

from apps.main.models import Ad, Category, Seller


class Command(BaseCommand):
    help = 'Генерация тестовых данных'

    def handle(self, *args, **options):
        UserFactory.create_batch(10)
        SellerFactory.create_batch(10)
        CategoryFactory.create_batch(3)
        AdFactory.create_batch(50)
        return 'Done.'


class UserFactory(factory.django.DjangoModelFactory):
    """Factory класс для пользователя."""

    email = factory.Faker('email')
    username = factory.LazyAttribute(lambda el: el.email.split('@')[0])
    password = factory.Faker('password')

    class Meta:
        model = User
        django_get_or_create = ('email', 'username', 'password')


class SellerFactory(factory.django.DjangoModelFactory):
    """Factory класс для продавца."""

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Seller
        django_get_or_create = ('user',)


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory класс для категории."""

    title = factory.Faker('sentence', nb_words=4)

    class Meta:
        model = Category
        django_get_or_create = ('title',)


class AdFactory(factory.django.DjangoModelFactory):
    """Factory класс для объявления."""

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=10)
    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(SellerFactory)
    price = factory.LazyAttribute(lambda _: random.randrange(1, 10000))

    class Meta:
        model = Ad
        django_get_or_create = ('title', 'description', 'category', 'seller', 'price')
