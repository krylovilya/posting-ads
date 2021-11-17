from django.urls import include, path

from apps.main.views import (AdCreateView, AdDetailView, AdsListView,
                             AdUpdateView, IndexView, SellerUpdateView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ads/', AdsListView.as_view(), name='ads-list'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('ads/add/', AdCreateView.as_view(), name='ad-create'),
    path('ads/<int:pk>/edit/', AdUpdateView.as_view(), name='ad-edit'),
    path('accounts/seller/', SellerUpdateView.as_view(), name='seller-update'),
]
