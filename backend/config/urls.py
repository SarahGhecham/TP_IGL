from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    home ,
    create_bilan_Bilologique ,
    create_bilan_Radiologique ,
    create_consultation ,
    create_examen ,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('dpi/<int:nss>/consultation', create_consultation, name='create_consultation'),
    path('dpi/consultation/<int:consultation_id>/bilanBiologique', create_bilan_Bilologique, name='create_bilan_biologique'),
    path('dpi/consultation/<int:consultation_id>/bilanRadiologique', create_bilan_Radiologique, name='create_bilan_radiologique'),
    path('dpi/consultation/<int:consultation_id>/bilanBiologique/examen', create_examen, name='create_examen'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)