from django.contrib import admin
from django.urls import path ,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Inclure les URLs de votre app avec le préfixe api/
    path('dpi/', include('dpi.urls')),  # Inclure les URLs de votre app avec le préfixe dpi/
]

