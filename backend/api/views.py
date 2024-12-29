from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from io import BytesIO

# Local imports
from .serializers import  *  # Specify individual serializers if possible
from .models import *  # Specify individual models if possible
from .qr_utils import generate_qr_code, scan_qr_code
from .permission import (
    DPIAccessPermission,
    DPIListAccessPermission,
    has_permission,
    is_Infermier,
    is_Laboratory,
    is_Radiologist,
    is_Pharmacien,
)



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




@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def DPI_list(request):
    permission = DPIListAccessPermission()
    if not permission.has_object_permission(request) :
        raise PermissionDenied("Vous n'avez pas la permission pour consulter les DPI.")
    
    if request.method == 'GET':
        user = request.user
        medecin = user.medecin
        dpi_Related = DPI.objects.filter(medecin_traitant=medecin)
        serializers = DPISerializer(dpi_Related, many=True)
        return Response(serializers.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DPI_detail(request , nss) :
    try:
        dpi = get_object_or_404(DPI , nss = nss)
    except Http404:
        return Response({"error": "Ce DPI n'existe pas."}, status=404)
    permission = DPIAccessPermission()
    if not permission.has_object_permission(request, dpi) :
        raise PermissionDenied("Vous n'avez pas la permission pour consulter cette DPI.") 
    serializer = DPISerializer(dpi)
    return Response(serializer.data)


#handle consulation
@api_view(['POST' , 'GET'])
@permission_classes([IsAuthenticated])
def consultation_list(request , nss):
    try:
        dpi = get_object_or_404(DPI, nss=nss)
    except Http404:
            return Response({"error": "Vous n'avez pas encore de DPI."}, status=404)
    
    if not has_permission(request, dpi=dpi):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter ces consultation.")
    
    if request.method == 'POST':
        
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dpi=dpi)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        serializer = ConsultationSerializer(dpi.consultations , many=True)
        return Response(serializer.data)    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def consultation_detail(request , consultation_id):
    try:
        consultation = get_object_or_404(Consultation, id=consultation_id)
    except Http404:
        return Response({"error": "La consultation n'existe pas."}, status=404)
    
    if not has_permission(request, consultation=consultation):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter cette consultation.")

    if request.method == 'GET':
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ConsultationSerializer(consultation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        consultation.delete()
        return Response(status=204) 


#handle bilan biologique

@api_view(['GET' ])
@permission_classes([IsAuthenticated])
def bilan_Bilologique_list(request ):
    if not is_Laboratory(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter les bilans biologiques.")
    
    if request.method == 'GET':
        serializers = BilanBiologiqueSerializer(BilanBiologique.objects.all(), many=True)
        return Response(serializers.data)
    

@api_view(['POST' , 'GET' , 'PUT' , 'DELETE'])
@permission_classes([IsAuthenticated])
def bilan_Bilologique_detail(request , consultation_id): 
    try:
        consultation = get_object_or_404(Consultation, id=consultation_id)
    except Http404:
        return Response({"error": "La consultation n'existe pas."}, status=404)
    user = request.user
    if not has_permission(request, consultation=consultation) and not is_Laboratory(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter ce bilan biologique.")

    if request.method == 'POST':
        request.data['consultation'] = consultation.id
        serializer = BilanBiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist :
            raise NotFound("Aucun bilan biologique n'existe pour cette consultation")
        serializer = BilanBiologiqueSerializer(bilan_biologique )
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan biologique associé à cette consultation."}, status=404)
        request.data['consultation'] = consultation.id
        serializer = BilanBiologiqueSerializer(bilan_biologique, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan biologique associé à cette consultation."}, status=404)
        bilan_biologique.delete()
        return Response(status=204)


# handle bilan radiologique
@api_view(['GET' ])
@permission_classes([IsAuthenticated])
def bilan_Radiologique_list(request ):
    if not is_Radiologist(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter les bilans radiologiques.")
    
    if request.method == 'GET':
        serializers = BilanRadiologiqueSerializer(BilanRadiologique.objects.all(), many=True)
        return Response(serializers.data)



@api_view(['POST' , 'GET' , 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def bilan_Radiologique_detail(request , consultation_id):
    try:
        consultation = get_object_or_404(Consultation, id=consultation_id)
    except Http404:
        return Response({"error": "La consultation n'existe pas."}, status=404)
    
    if not has_permission(request, consultation=consultation) and not is_Radiologist(request) :
        raise PermissionDenied("Vous n'avez pas la permission pour consulter ce bilan radiologique.")
    
    if request.method == 'POST':
        request.data['consultation'] = consultation.id
        serializer = BilanRadiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            bilan_Radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            raise NotFound("Aucun bilan radiologique n'existe pour cette consultation")
        serializer = BilanRadiologiqueSerializer(bilan_Radiologique)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            bilan_radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan radiologique associé à cette consultation."}, status=404)
        request.data['consultation'] = consultation.id
        serializer = BilanRadiologiqueSerializer(bilan_radiologique, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            bilan_radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan radiologique associé à cette consultation."}, status=404)
        bilan_radiologique.delete()
        return Response(status=204)
    

#handles examen biologique
@api_view(['POST' , 'GET'])
@permission_classes([IsAuthenticated])
def examen_list(request , bilan_id):
    try:
        bilan = get_object_or_404(BilanBiologique, id=bilan_id)
    except Http404:
        return Response({"error": "Aucun bilan biologique n'existe pour cette consultation."}, status=404)
    
    if not has_permission(request, bilan = bilan) and not is_Laboratory(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter les examens.")
    
    if request.method == 'POST':
        serializer = ExamenBiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bilan=bilan)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    if request.method == 'GET':
        serializer = ExamenBiologiqueSerializer(bilan.examens , many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def examen_detail(request , examen_id):
    try:
        examen = get_object_or_404(ExamenBiologique, id=examen_id)
    except Http404:
        return Response({"error": "L'examen n'existe pas."}, status=404)
    
    if not has_permission(request, examen=examen) and not is_Laboratory(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter cet examen.")
    
    if request.method == 'GET':
        serializer = ExamenBiologiqueSerializer(examen)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = ExamenBiologiqueSerializer(examen, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        examen.delete()
        return Response(status=204)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ordonnance_list(request):
    if not is_Pharmacien(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter les ordonnances.")
    if request.method == 'GET':
        serializers = OrdonnanceSerializer(Ordonnance.objects.all(), many=True)
        return Response(serializers.data)
    
@api_view(['put' , 'GET'])
@permission_classes([IsAuthenticated])
def ordonnance_detail(request , ordonnance_id):
    try:
        ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)
    except Http404:
        return Response({"error": "L'ordonnance n'existe pas."}, status=404)
    
    
    if not has_permission(request, ordonnance=ordonnance) and not is_Pharmacien(request):
        raise PermissionDenied("Vous n'avez pas la permission pour consulter cette ordonnance.")
    
    if request.method == 'PUT':
        request.data['valid'] = True
        serializer = OrdonnanceSerializer(ordonnance, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    if request.method == 'GET':
        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data)    
        
    
