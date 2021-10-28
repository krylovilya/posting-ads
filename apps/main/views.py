from constance import config
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from apps.main.models import Ad, Tag


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
