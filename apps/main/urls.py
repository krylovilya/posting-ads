from django.urls import include, path

from apps.main.views import (AdDetailView, AdsListView, IndexView,
                             SellerUpdateView)

urlpatterns = [
    path('', IndexView.as_view()),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ads/', AdsListView.as_view()),
    path('ads/<int:pk>/', AdDetailView.as_view()),
    path('accounts/seller/', SellerUpdateView.as_view()),
]
