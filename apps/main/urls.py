from django.urls import include, path

from apps.main.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('pages/', include('django.contrib.flatpages.urls')),
]
