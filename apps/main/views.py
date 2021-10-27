from constance import config
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """Главная страница"""

    template_name = "main/index.html"
    extra_context = {'turn_on_block': config.MAINTENANCE_MODE}
