from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models import Consultation,Soin,ResultatExamenImagerie,CompteRendu,Infirmier

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

# Local imports
from .serializers import  *  # Specify individual serializers if possible
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

class SoinListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Soin.objects.all()
    serializer_class = SoinSerializer

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

class SoinCreateView(generics.ListCreateAPIView):
    queryset = Soin.objects.all()
    serializer_class = SoinSerializer

    def perform_create(self, serializer):
        infirmier_default = Infirmier.objects.get(id=1)
        serializer.save(infirmier=infirmier_default)


class SoinDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Soin.objects.all()
    serializer_class = SoinSerializer
    lookup_field = 'id'

class DeleteConsultationView(generics.DestroyAPIView):
    queryset = Consultation.objects.all()
    lookup_field = 'id'

class ConsultationListView(generics.ListAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

class CreateConsultationView(generics.CreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

class ConsultationResumeView(APIView):
    permission_classes = [AllowAny]
    def patch(self, request, pk):
        try:
            consultation = Consultation.objects.get(pk=pk)
        except Consultation.DoesNotExist:
            return Response({"error": "Consultation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ConsultationSerializer(consultation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResultatExamenImagerieListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        resultats = ResultatExamenImagerie.objects.all()
        serializer = ResultatExamenImagerieSerializerForGet(resultats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ResultatExamenImagerieCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = ResultatExamenImagerie.objects.all()
    serializer_class = ResultatExamenImagerieSerializer



class CompteRenduCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CompteRendu.objects.all()
    serializer_class = CompteRenduSerializer

    def perform_create(self, serializer):
        resultat_examen_id = self.kwargs['resultat_examen_id']
        resultat_examen = ResultatExamenImagerie.objects.get(id=resultat_examen_id)
        serializer.save(resultat_examen=resultat_examen)


class ResultatExamenImagerieUpdateView(generics.UpdateAPIView):
    queryset = ResultatExamenImagerie.objects.all()
    serializer_class = ResultatExamenImagerieSerializer


class CompteRenduUpdateView(generics.UpdateAPIView):
    queryset = CompteRendu.objects.all()
    serializer_class = CompteRenduSerializer


class ResultatExamenImagerieDeleteView(generics.DestroyAPIView):
    queryset = ResultatExamenImagerie.objects.all()
    lookup_field = 'pk'

class ResultatExamenImagerieDetailView(generics.RetrieveAPIView):
    queryset = ResultatExamenImagerie.objects.all()
    serializer_class = ResultatExamenImagerieSerializerForGet
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):

        try:
            result = self.get_object()
            serializer = self.get_serializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ResultatExamenImagerie.DoesNotExist:
            return Response({"detail": "ResultatExamenImagerie not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST' , 'GET' , 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def bilan_Radiologique_detail(request , consultation_id):
    try:
        consultation = get_object_or_404(Consultation, id=consultation_id)
    except Http404:
        return Response({"error": "La consultation n'existe pas."}, status=404)
    
    if request.method == 'POST':
        request.data['consultation'] = consultation.id
        serializer = BilanRadiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            bilan_radiologique = serializer.save(consultation=consultation)
            # Here, you should save the ResultatExamenImagerie if it's not already included in the POST body.
            # The resultats will be created automatically by the serializer as defined above.
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    if request.method == 'GET':
        try:
            bilan_Radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            raise NotFound("Aucun bilan radiologique n'existe pour cette consultation")
        serializer = BilanRadiologiqueSerializer(bilan_Radiologique)
        return Response(serializer.data)

# handle bilan radiologique
@api_view(['GET' ])
@permission_classes([AllowAny])
def bilan_Radiologique_list(request ):
    # if not is_Radiologist(request):
    #     raise PermissionDenied("Vous n'avez pas la permission pour consulter les bilans radiologiques.")
    
    if request.method == 'GET':
        serializers = BilanRadiologiqueSerializer(BilanRadiologique.objects.all(), many=True)
        return Response(serializers.data)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def examen_list(request, bilan_id):
    try:
        bilan = get_object_or_404(BilanRadiologique, id=bilan_id)
    except Http404:
        return Response({"error": "Aucun bilan radiologique n'existe pour cette consultation."}, status=404)

    if request.method == 'POST':
        # Create new ResultatExamenImagerie linked to this BilanRadiologique
        serializer = ResultatExamenImagerieSerializer(data=request.data)
        if serializer.is_valid():
            # Save the ResultatExamenImagerie instance
            resultat = serializer.save()

            # Add the newly created ResultatExamenImagerie to the resultats field of BilanRadiologique
            bilan.resultats.add(resultat)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    if request.method == 'GET':
        # Retrieve all ResultatExamenImagerie objects related to this BilanRadiologique
        resultats = bilan.resultats.all()
        serializer = ResultatExamenImagerieSerializer(resultats, many=True)
        return Response(serializer.data)
