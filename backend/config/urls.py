from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    DPI_list ,
    DPI_detail ,
    bilan_Bilologique_detail ,
    bilan_Radiologique_detail ,
    consultation_list ,
    consultation_detail ,
    examen_list ,
    examen_detail ,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dpi/',DPI_list, name='DPI_list'),
    path('dpi/<int:nss>/', DPI_detail, name='DPI_detail'),
    path('dpi/<int:nss>/consultation/', consultation_list, name='consultation_list'),
    path('dpi/consultation/<int:consultation_id>/', consultation_detail, name='consultation_detail'),
    path('dpi/consultation/<int:consultation_id>/bilanBiologique/', bilan_Bilologique_detail, name='bilan_biologique_detail'),
    path('dpi/consultation/<int:consultation_id>/bilanRadiologique/', bilan_Radiologique_detail, name='bilan_radiologique_detail'), 
    path('dpi/consultation/<int:consultation_id>/bilanBiologique/examen/', examen_list, name='examen_list'), 
    path('dpi/consultation/bilanBiologique/examen/<int:examen_id>/', examen_detail, name='examen_detail'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)