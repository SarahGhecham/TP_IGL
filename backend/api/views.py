from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated # Permet l'accès à tous
from .models import DPI, Medecin,ExamenBiologique
from django.contrib.auth.models import User
from .serializers import DPISerializer, RoleSignupSerializer
from rest_framework.exceptions import NotFound
from django.http import JsonResponse,HttpResponse
from .qr_utils import generate_qr_code, scan_qr_code
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission






#utilitaire pour les permissions
class IsMedecin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'medecin')


# Authentication methods

#Signup view
class RoleSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RoleSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Login View
class RoleBasedLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Get the user's role
                role = None
                if hasattr(user, 'medecin'):
                    role = 'medecin'
                elif hasattr(user, 'infirmier'):
                    role = 'infirmier'
                elif hasattr(user, 'laborantin'):
                    role = 'laborantin'
                elif hasattr(user, 'radiologue'):
                    role = 'radiologue'
                elif hasattr(user, 'administratif'):
                    role = 'administratif'
                elif hasattr(user, 'patient'):
                    role = 'patient'

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': role  
                })
                print(f'${username} logged in , role: ${role}')
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token or token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)


#DPI views

#creer un DPI
class CreateDPIView(APIView):
    permission_classes = [IsAuthenticated,IsMedecin]

    def post(self, request):
        serializer = DPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#recuperer un DPI
class RetrieveDPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dpi_id):
        try:
            dpi = DPI.objects.get(id=dpi_id)
            serializer = DPISerializer(dpi)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DPI.DoesNotExist:
            return Response({"error": "DPI not found"}, status=status.HTTP_404_NOT_FOUND)

#récuperer tout les dpis


 
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
        if not hasattr(self.request.user, 'medecin'):
            raise NotFound("Accès non autorisé. Seul un médecin peut accéder à ce DPI.")
        """
        
        # Chercher le DPI par NSS
        try:
            dpi = DPI.objects.get(nss=nss)
        except DPI.DoesNotExist:
            raise NotFound("DPI non trouvé avec ce NSS.")
        
        return dpi
