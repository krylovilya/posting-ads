from random import randint, uniform

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from constance import config

from apps.main.forms import ImageFormset, SellerForm, UserForm
from apps.main.models import Ad, Seller, SMSLog, Tag
from apps.main.tasks import send_confirmation_code_by_sms


class IndexView(TemplateView):
    """Главная страница."""

    template_name = "main/index.html"
    extra_context = {'turn_on_block': config.MAINTENANCE_MODE}


@method_decorator(cache_page(60), name='dispatch')
class AdsListView(ListView):
    """Список объявлений."""

    model = Ad
    template_name = "main/ad_list.html"
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        kwargs.update({
            'tags': Tag.objects.get_queryset(),
            'current_tag': self.request.GET.get('tag', '')
        })
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag', None)
        if tag:
            return queryset.filter(tags__slug=tag)
        return queryset


@method_decorator(cache_page(60), name='dispatch')
class AdDetailView(DetailView):
    """Детальная информация об объявлении."""

    model = Ad
    template_name = "main/ad_detail.html"

    def get_context_data(self, **kwargs):
        price_factor = cache.get('price_factor')
        if price_factor is None:
            price_factor = round(uniform(0.8, 1.2), 1)
            cache.set('price_factor', price_factor, 60)
        kwargs['price_factor'] = price_factor
        return super().get_context_data(**kwargs)


class SellerUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление информации об продавце."""

    model = Seller
    template_name = "main/seller_update.html"
    success_url = '/?seller_update_success=1'
    login_url = ' /accounts/login/'
    form_class = SellerForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        if self.request.POST:
            user_form = UserForm(data=self.request.POST)
        else:
            user_form = UserForm(instance=self.request.user)
        kwargs.update({
            'form': self.get_form(),
            'user_form': user_form,
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, seller_form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if not user_form.is_valid():
            raise ValidationError('User form is not valid')
        user_form.save()
        seller_form.save()
        return HttpResponseRedirect(self.get_success_url())


class AdViewMixin(ModelFormMixin, LoginRequiredMixin, ProcessFormView):
    """Миксин для отображения форм объявлений."""

    model = Ad
    fields = ('title', 'description', 'category', 'tags', 'price')
    template_name = 'main/ad_create.html'
    login_url = ' /accounts/login/'
    page_title = ''

    def form_valid(self, form):
        seller = Seller.objects.get(user=self.request.user)
        form.instance.seller = seller
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'page_title': self.page_title,
            'image_formset': ImageFormset(instance=self.object)
        })
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.seller.is_banned:
            raise Http404('У вас недостаточно прав для добавления/изменения объявлений')
        response = super().post(request, args, kwargs)
        image_formset = ImageFormset(data=request.POST, files=request.FILES, instance=self.object)
        if image_formset.is_valid():
            for image_form in image_formset:
                image_form.save()
        return response

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        seller = Seller.objects.get(user=self.request.user)
        if obj.seller.pk != seller.pk:
            raise Http404('Нет доступа к данному объекту')
        return obj


class AdCreateView(AdViewMixin, CreateView):
    """Отобразить форму создания объявления."""

    page_title = 'Создание объявления'
    success_url = '/?ad_create_success=1'


class AdUpdateView(AdViewMixin, UpdateView):
    """Отобразить форму редактирования объявления."""

    page_title = 'Редактирование объявления'
    success_url = '/?ad_update_success=1'


class SendSmsView(View):
    """Обрабатывает fetch запрос на отправку кода из смс"""

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        seller = Seller.objects.get(user_id=user_id)
        phone = self.request.GET.get('phone')
        confirmation_code = randint(1000, 9999)
        sms_log, _ = SMSLog.objects.update_or_create(seller_id=seller.id, defaults={
            'code': confirmation_code,
            'sent_phone': phone,
        })
        send_confirmation_code_by_sms.delay(phone, confirmation_code)
        return HttpResponse('', status=200)
