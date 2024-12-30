from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # DPI-related paths
    path('patients/', FirstThreePatientsView.as_view(), name='first-three-patients'),
    path('search-dpi-by-nss/<str:nss>/', SearchDPIByNSSView.as_view(), name='search-dpi-by-nss'),
    path('search-dpi-by-qr/', SearchDPIByQRView.as_view(), name='search-dpi-by-qr'),
    path('dpi/', DPI_list, name='DPI_list'),
    path('dpi/<int:dpi_id>/', RetrieveDPIView.as_view(), name='retrieve_dpi'),
    path('dpi/<int:nss>/', DPI_detail, name='DPI_detail'),
    path('dpi/create/', CreateDPIView.as_view(), name='create_dpi'),
    path('dpi/delete/username/<str:username>/', DeleteDPIByUsernameView.as_view(), name='delete_dpi_by_username'),
    path('dpi/<int:dpi_id>/<str:examen_type>/', generate_trend_graph, name='generate_trend_graph'),

    # Consultation-related paths
    path('dpi/<int:nss>/consultation/', consultation_list, name='consultation_list'),
    path('dpi/consultation/<int:consultation_id>/', consultation_detail, name='consultation_detail'),
    path('dpi/consultation/<int:consultation_id>/bilanBiologique/', bilan_Bilologique_detail, name='bilan_biologique_detail'),
    path('dpi/consultation/<int:consultation_id>/bilanRadiologique/', bilan_Radiologique_detail, name='bilan_radiologique_detail'),                 path('dpi/consultation/create',create_consultation,name='create_consultation'),
    
    # Ordonnance-related paths
    path('ordonnance/', ordonnance_list, name='ordonnance_list'),
    path('dpi/consultation/ordonnance/create/',create_ordonnance ,  name='create_ordonnance'),
    path('dpi/consultation/ordonnance/<int:ordonnance_id>/', ordonnance_detail, name='ordonnance_detail'),

    # Bilan and examen-related paths
    path('bilanBiologique/', bilan_Bilologique_list, name='bilan_biologique_list'),
    path('bilanRadiologique/', bilan_Radiologique_list, name='bilan_radiologique_list'),
    path('dpi/consultation/bilanBiologique/<int:bilan_id>/examen/', examen_list, name='examen_list'),
    path('dpi/consultation/bilanBiologique/examen/<int:examen_id>/', examen_detail, name='examen_detail'),

    # Authentication and authorization paths
    path('signup/', RoleSignupView.as_view(), name='signup'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
