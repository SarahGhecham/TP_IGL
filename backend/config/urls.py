from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    home ,
    create_bilan_Bilologique ,
    create_bilan_Radiologique ,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('dpi/consultation/<int:consultation_id>/bilan/Biologique', create_bilan_Bilologique, name='create_bilan_biologique'),
    path('dpi/consultation/<int:consultation_id>/bilan/Radiologique', create_bilan_Radiologique, name='create_bilan_radiologique'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)