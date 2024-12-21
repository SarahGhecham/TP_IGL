from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny  # Permet l'accès à tous
from .models import DPI, Medecin
from .serializers import DPISerializer
from rest_framework.exceptions import NotFound

class SearchDPIByNSSView(generics.RetrieveAPIView):
    queryset = DPI.objects.all()
    serializer_class = DPISerializer
    permission_classes = [AllowAny]  # permission_classes = [IsAuthenticated]

    def get_object(self):
        # Récupérer le NSS depuis les paramètres de l'URL
        nss = self.kwargs['nss']

        """
        # Vérifier si l'utilisateur est un médecin
        if not hasattr(self.request.user, 'medecin'):
            raise NotFound("Accès non autorisé. Seul un médecin peut accéder à ce DPI.")
        """
        
        # Chercher le DPI par NSS
        try:
            dpi = DPI.objects.get(nss=nss)
        except DPI.DoesNotExist:
            raise NotFound("DPI non trouvé avec ce NSS.")
        
        return dpi
