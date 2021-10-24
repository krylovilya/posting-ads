from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Seller(models.Model):
    """Модель Продавец."""

    user = models.OneToOneField(to=User, verbose_name="пользователь", on_delete=models.CASCADE, related_name='seller')

    @property
    def num_ads(self):
        return self.ads.count()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'


class Category(models.Model):
    """Модель Категория."""

    title = models.CharField(verbose_name='заголовок категории', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='семантический url', max_length=128, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tag(models.Model):
    """Модель Тэг."""

    title = models.CharField(verbose_name='заголовок тэга', max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'


class Ad(models.Model):
    """Модель Объявление."""

    title = models.CharField(verbose_name='заголовок объявления', max_length=128)
    description = models.CharField(verbose_name='описание объявления', max_length=2048, null=True)
    category = models.ForeignKey(to=Category, verbose_name='категория', on_delete=models.CASCADE, related_name='ads')
    seller = models.ForeignKey(to=Seller, verbose_name='продавец', on_delete=models.CASCADE, related_name='ads')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    tags = models.ManyToManyField(to=Tag, verbose_name='тэги', related_name='ads')

    def __str__(self):
        return f'{self.title} [{self.seller.user}]'

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
