from django.urls import include, path

from apps.main.views import (AdCreateView, AdDetailView, AdsListView,
                             AdUpdateView, IndexView, SellerUpdateView)

urlpatterns = [
    path('', IndexView.as_view()),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ads/', AdsListView.as_view()),
    path('ads/<int:pk>/', AdDetailView.as_view()),
    path('ads/add/', AdCreateView.as_view()),
    path('ads/<int:pk>/edit/', AdUpdateView.as_view()),
    path('accounts/seller/', SellerUpdateView.as_view()),
]
