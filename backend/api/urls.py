# api/urls.py
from django.urls import path
from .views import SearchDPIByNSSView

urlpatterns = [
    path('dpi/<str:nss>/', SearchDPIByNSSView.as_view(), name='search-dpi-by-nss'),
]
