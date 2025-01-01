from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from api.models import Consultation,Soin,ResultatExamenImagerie,CompteRendu,Infirmier
from .serializers import ConsultationSerializer,ResultatExamenImagerieSerializerForGet,SoinSerializer,CompteRenduSerializer,ResultatExamenImagerieSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action



class SoinListView(generics.ListCreateAPIView):
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
    def get(self, request, *args, **kwargs):
        resultats = ResultatExamenImagerie.objects.all()
        serializer = ResultatExamenImagerieSerializerForGet(resultats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ResultatExamenImagerieCreateView(generics.CreateAPIView):
    queryset = ResultatExamenImagerie.objects.all()
    serializer_class = ResultatExamenImagerieSerializer



class CompteRenduCreateView(generics.CreateAPIView):
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