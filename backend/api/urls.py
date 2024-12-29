from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('search-dpi-by-nss/<str:nss>/', SearchDPIByNSSView.as_view(), name='search-dpi-by-nss'),
    path('search-dpi-by-qr/', SearchDPIByQRView.as_view(), name='search-dpi-by-qr'),
    path('dpi/<int:dpi_id>/trend/<str:examen_type>/',generate_trend_graph, name='generate_trend_graph'),
    #auth paths 
    path('signup/', RoleSignupView.as_view(), name='signup'),
    path('login/', RoleBasedLoginView.as_view(), name='login'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    #refresh jwt token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #dpi paths
    path('dpi/create/', CreateDPIView.as_view(), name='create_dpi'),
    path('dpi/<int:dpi_id>/', RetrieveDPIView.as_view(), name='retrieve_dpi'),
    path('dpi/delete/username/<str:username>/', DeleteDPIByUsernameView.as_view(), name='delete_dpi_by_username')
]

