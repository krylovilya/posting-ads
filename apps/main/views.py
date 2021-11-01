from constance import config
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from apps.main.models import Ad


class IndexView(TemplateView):
    """Главная страница."""

    template_name = "main/index.html"
    extra_context = {'turn_on_block': config.MAINTENANCE_MODE}


class AdsListView(ListView):
    """Список объявлений."""

    model = Ad
    template_name = "main/ad_list.html"

    def get_context_data(self, *args, **kwargs):
        kwargs.update({'ads': self.get_queryset()})
        return super().get_context_data(*args, **kwargs)


class AdDetailView(DetailView):
    """Детальная информация об объявлении."""

    model = Ad
    template_name = "main/ad_detail.html"
