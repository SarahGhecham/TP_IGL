from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from .serializers import *
from .models import *




class RedactionBilanView(APIView):
    pass

@api_view(['GET'])
def home(request):
    context = {
        'title': 'Bienvenue sur le site de l\'API',
    }
    return Response(context)


@api_view(['POST'])
def create_consultation(request):
    pass

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



@api_view(['POST'])
def create_examen(request , consultation_id):
    try:
        consultation = get_object_or_404(Consultation, id=consultation_id)
    except Exception as e:
        raise NotFound("La consultation n'existe pas")
    try:
        bilan = get_object_or_404(BilanBiologique, consultation=consultation)
    except Exception as e:
        raise NotFound("Aucun bilan biologique n'existe pour cette consultation")
    serializer = ExamenBiologiqueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(bilan=bilan)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)