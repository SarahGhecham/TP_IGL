from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny # Permet l'accès à tous
from .models import DPI,ExamenBiologique
from .serializers import DPISerializer
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from .qr_utils import scan_qr_code
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import get_object_or_404


def generate_trend_graph(request, dpi_id, examen_type):
    # Récupérer le DPI par ID
    dpi = get_object_or_404(DPI, id=dpi_id)

    # Filtrer les examens biologiques pour le DPI et le type d'examen (glycémie, cholestérol, etc.)
    examens = ExamenBiologique.objects.filter(bilan__consultation__dpi=dpi, type_examen=examen_type).order_by('date_examen')

    if not examens:
        return JsonResponse({"message": "Aucun examen trouvé pour ce DPI et ce type d'examen."}, status=404)

    # Extraire les dates et les résultats
    dates = [examen.date_examen.strftime('%Y-%m-%d') for examen in examens]
    resultats = [examen.resultat for examen in examens]
    patient=dpi.patient.user.get_full_name()

    # Retourner les données sous forme de JSON
    return JsonResponse({
        "dates": dates,
        "resultats": resultats,
        "examen_type": examen_type,
        "patient": patient,
    })


class SearchDPIByQRView(APIView):
    permission_classes = [AllowAny]  # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Vérification du fichier QR envoyé dans la requête
        file = request.FILES.get('file')

        if not file:
            return Response({"detail": "Aucun fichier QR Code trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarder l'image temporairement
        image_path = fr"api\qr_imgs\{file.name}"
        with open(image_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Décoder le QR Code pour obtenir le NSS
        nss = scan_qr_code(image_path)

        if not nss:
            return Response({"detail": "QR Code non valide ou NSS non trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        # Chercher le DPI en fonction du NSS
        try:
            dpi = DPI.objects.get(nss=nss)
        except DPI.DoesNotExist:
            return Response({"detail": "DPI non trouvé pour ce NSS."}, status=status.HTTP_404_NOT_FOUND)

        # Sérialiser les données du DPI
        serializer = DPISerializer(dpi)

        return Response(serializer.data, status=status.HTTP_200_OK)



class SearchDPIByNSSView(generics.RetrieveAPIView):
    queryset = DPI.objects.all()
    serializer_class = DPISerializer
    permission_classes = [AllowAny]  # permission_classes = [IsAuthenticated]

    def get_object(self):
        # Récupérer le NSS depuis les paramètres de l'URL
        nss = self.kwargs['nss']

        """
        # Vérifier si l'utilisateur est un médecin
        if not hasattr(self.request.user,'):
            raise NotFound("Accès non autorisé. Seul un médecin peut accéder à ce DPI.")
        """
        
        # Chercher le DPI par NSS
        try:
            dpi = DPI.objects.get(nss=nss)
        except DPI.DoesNotExist:
            raise NotFound("DPI non trouvé avec ce NSS.")
        
        return dpi
