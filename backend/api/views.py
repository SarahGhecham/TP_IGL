from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from .serializers import BilanBiologiqueSerializer , ConsultationSerializer , BilanRadiologiqueSerializer
from .models import Consultation




class RedactionBilanView(APIView):
    pass

@api_view(['GET'])
def home(request):
    context = {
        'title': 'Bienvenue sur le site de l\'API',
    }
    return Response(context)



@api_view(['POST'])
def create_bilan_Bilologique(request , consultation_id):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        raise NotFound("La consultation n'existe pas")
    request.data['consultation'] = consultation.id
    serializer = BilanBiologiqueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(consultation=consultation)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def create_bilan_Radiologique(request , consultation_id):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        raise NotFound("La consultation n'existe pas")
    request.data['consultation'] = consultation.id
    serializer = BilanRadiologiqueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(consultation=consultation)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)