from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """Главная страница"""

    template_name = "main/index.html"
