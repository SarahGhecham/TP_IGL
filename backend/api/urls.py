# api/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('search-dpi-by-nss/<str:nss>/', SearchDPIByNSSView.as_view(), name='search-dpi-by-nss'),
    path('search-dpi-by-qr/', SearchDPIByQRView.as_view(), name='search-dpi-by-qr'),
    path('dpi/<int:dpi_id>/trend/<str:examen_type>/',generate_trend_graph, name='generate_trend_graph'),
    path('dpi/',DPI_list, name='DPI_list'),
    path('dpi/<int:nss>/', DPI_detail, name='DPI_detail'),
    path('dpi/<int:nss>/consultation/', consultation_list, name='consultation_list'),
    path('ordonnance/', ordonnance_list, name='ordonnance_list'),
    path('dpi/consultation/ordonnance/<int:ordonnance_id>/', ordonnance_detail, name='ordonnance_detail'),
    path('dpi/consultation/<int:consultation_id>/', consultation_detail, name='consultation_detail'),
    path('dpi/consultation/<int:consultation_id>/bilanBiologique/', bilan_Bilologique_detail, name='bilan_biologique_detail'),
    path('dpi/consultation/<int:consultation_id>/bilanRadiologique/', bilan_Radiologique_detail, name='bilan_radiologique_detail'), 
    path('dpi/consultation/bilanBiologique/<int:bilan_id>/examen/', examen_list, name='examen_list'),  
    path('dpi/consultation/bilanBiologique/examen/<int:examen_id>/', examen_detail, name='examen_detail'),

    # for role laborontin and radiologue
    path('bilanBiologique/', bilan_Bilologique_list, name='bilan_biologique_list'),
    path('bilanRadiologique/', bilan_Radiologique_list, name='bilan_radiologique_list'),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
