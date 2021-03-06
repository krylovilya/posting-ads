from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify

from apps.main.services.validate_itn import validate_itn


class BaseModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    class Meta:
        abstract = True


class Seller(models.Model):
    """Модель Продавец."""

    user = models.OneToOneField(to=User, verbose_name="пользователь", on_delete=models.CASCADE, related_name='seller')
    itn = models.CharField(verbose_name='идентификационный номер налогоплательщика', max_length=12,
                           validators=(validate_itn,))
    avatar = models.ImageField(verbose_name='аватар пользователя', upload_to='avatars', default='default.jpg')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Неверный номер телефона.")
    phone = models.CharField(verbose_name='номер телефона (в формате +7)',
                             validators=(phone_regex,), max_length=12, blank=True)

    @property
    def num_ads(self):
        return self.ads.count()

    @property
    def is_banned(self):
        return self.user.groups.filter(name='banned users').exists()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'


class Category(BaseModel):
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


class Tag(BaseModel):
    """Модель Тэг. Временно не используется."""

    title = models.CharField(verbose_name='заголовок тэга', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='семантический url', max_length=128, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'


class Ad(BaseModel):
    """Модель Объявление."""

    title = models.CharField(verbose_name='заголовок объявления', max_length=128)
    description = models.CharField(verbose_name='описание объявления', max_length=2048, null=True)
    category = models.ForeignKey(to=Category, verbose_name='категория', on_delete=models.CASCADE, related_name='ads')
    seller = models.ForeignKey(to=Seller, verbose_name='продавец', on_delete=models.CASCADE, related_name='ads')
    tags = ArrayField(models.CharField(max_length=10, blank=True), verbose_name='тэги', null=True)
    price = models.PositiveIntegerField(verbose_name='цена', default=0)
    archive = models.BooleanField(verbose_name='в архиве', default=False)

    def __str__(self):
        return f'{self.title} [{self.seller.user}]'

    @property
    def url(self):
        site_url = Site.objects.get_current().domain
        return site_url + reverse_lazy('ad-detail', args=(self.id,))

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'


class ArchiveAdsManager(models.Manager):
    """Менеджер, возвращающий архивные объявления."""

    def get_queryset(self):
        return Ad.objects.filter(archive=True)


class ArchiveAds(Ad):
    """Прокси-модель для архивных объявлений."""

    class Meta:
        proxy = True

    archive = ArchiveAdsManager()


class Picture(models.Model):
    """Модель Изображение объявления."""

    ad = models.ForeignKey(to=Ad, verbose_name='объявление', on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(verbose_name='изображение объявления', upload_to='ads_pictures')

    class Meta:
        verbose_name = 'изображение объявления'
        verbose_name_plural = 'изображения объявлений'


class Subscription(models.Model):
    """Подписки на объявления."""

    title = models.CharField(verbose_name='заголовок подписки', max_length=128)
    user = models.ManyToManyField(to=User, verbose_name='пользователи', related_name='users')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class SMSLog(models.Model):
    """Модель связывает продавца и код из смс"""

    seller = models.OneToOneField(to=Seller, verbose_name="продавец", on_delete=models.CASCADE,
                                  related_name='smslog')
    code = models.PositiveIntegerField(verbose_name='проверочный код, 4 цифры', validators=(
        MaxValueValidator(9999),
        MinValueValidator(1000),
    ))
    sent_phone = models.CharField(verbose_name='номер телефона, на который отправлен смс', max_length=12, blank=True)
    confirmed = models.BooleanField(verbose_name='номер подтверждён', default=False)

    class Meta:
        verbose_name = 'смс подтверждение'
        verbose_name_plural = 'смс подтверждения'
