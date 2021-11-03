from constance import config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

from apps.main.forms import SellerForm, UserForm
from apps.main.models import Ad, Seller, Tag


class IndexView(TemplateView):
    """Главная страница."""

    template_name = "main/index.html"
    extra_context = {'turn_on_block': config.MAINTENANCE_MODE}


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


class AdDetailView(DetailView):
    """Детальная информация об объявлении."""

    model = Ad
    template_name = "main/ad_detail.html"


class SellerUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление информации об продавце."""

    model = Seller
    template_name = "main/seller_update.html"
    success_url = '/?seller_update_success=1'
    login_url = '/'
    form_class = SellerForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        kwargs.update({
            'seller_form': SellerForm(self.request.POST, instance=self.request.user),
            'user_form': UserForm(self.request.POST, instance=self.get_object()),
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, seller_form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if not user_form.is_valid():
            raise ValidationError('User form is not valid')
        user_form.save()
        seller_form.save()
        return HttpResponseRedirect(self.get_success_url())


class AdCreateView(CreateView):
    model = Ad
    fields = ('title', 'description', 'category', 'tags', 'price')
    template_name = 'main/ad_create.html'
    success_url = '/?ad_create_success=1'

    def form_valid(self, form):
        seller = Seller.objects.filter(user=self.request.user).first()
        form.instance.seller = seller
        return super().form_valid(form)


class AdUpdateView(UpdateView):
    model = Ad
    fields = ('title', 'description', 'category', 'tags', 'price')
    template_name = 'main/ad_update.html'
    success_url = '/?ad_update_success=1'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        seller = Seller.objects.get(user=self.request.user)
        if obj.seller.pk != seller.pk:
            raise PermissionError('Нет доступа к изменению данного объекта')
        return obj
