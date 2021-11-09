from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    # name = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    class Meta:
        abstract = True


class Seller(models.Model):
    """Модель Продавец."""

    user = models.OneToOneField(to=User, verbose_name="пользователь", on_delete=models.CASCADE, related_name='seller')
    itn = models.CharField(verbose_name='идентификационный номер налогоплательщика', max_length=12)
    avatar = models.ImageField(verbose_name='аватар пользователя', upload_to='avatars', default='default.jpg')

    @property
    def num_ads(self):
        return self.ads.count()

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
    """Модель Тэг."""

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
    tags = models.ManyToManyField(to=Tag, verbose_name='тэги', related_name='ads')
    price = models.PositiveIntegerField(verbose_name='цена', default=0)
    archive = models.BooleanField(verbose_name='в архиве', default=False)

    def __str__(self):
        return f'{self.title} [{self.seller.user}]'

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
