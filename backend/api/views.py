from django.shortcuts import render , get_object_or_404 
from django.http import Http404 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound , PermissionDenied
from .serializers import *
from .models import *



@api_view(['GET'])
def DPI_list(request):
    user = request.user
    if hasattr(user , 'medecin'):
        pass
    else:
        raise PermissionDenied("Vous n'avez pas la permission de consulter les DPI.")
    if request.method == 'GET':
        serializers = DPISerializer(DPI.objects.all(), many=True)
        return Response(serializers.data)

@api_view(['GET'])
def DPI_detail(request , nss) :
    try:
        dpi = get_object_or_404(DPI , nss = nss)
        user = request.user
        if hasattr(user , 'patient'):
            if request.method != 'GET':
                raise PermissionDenied("Vous n'avez pas la permission de modifier cette DPI.")
        elif hasattr(user , 'medecin'):
            pass
        else:
            raise PermissionDenied("Vous n'avez pas la permission pour consulter cette DPI.")
    except Http404:
        return Response({"error": "Ce DPI n'existe pas."}, status=404)
    serializer = DPISerializer(dpi)
    return Response(serializer.data)


#handle consulation
@api_view(['POST' , 'GET'])
def consultation_list(request , nss):
    if request.method == 'POST':
        try:
            dpi = get_object_or_404(DPI, nss=nss)
        except Http404:
            return Response({"error": "Vous n'avez pas encore de DPI."}, status=404)
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dpi=dpi)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            dpi = get_object_or_404(DPI, nss=nss)
        except Http404:
            return Response({"error": "Vous n'avez pas encore de DPI."}, status=404)
        serializer = ConsultationSerializer(dpi.consultations , many=True)
        return Response(serializer.data)    

@api_view(['GET', 'PUT', 'DELETE'])
def consultation_detail(request , consultation_id):
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        serializer = ConsultationSerializer(consultation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        consultation.delete()
        return Response(status=204) 


#handle bilan biologique
@api_view(['POST' , 'GET' , 'PUT' , 'DELETE'])
def bilan_Bilologique_detail(request , consultation_id): 
    if request.method == 'POST':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        request.data['consultation'] = consultation.id
        serializer = BilanBiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist :
            raise NotFound("Aucun bilan biologique n'existe pour cette consultation")
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        serializer = BilanBiologiqueSerializer(bilan_biologique )
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan biologique associé à cette consultation."}, status=404)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        request.data['consultation'] = consultation.id
        serializer = BilanBiologiqueSerializer(bilan_biologique, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan biologique associé à cette consultation."}, status=404)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        bilan_biologique.delete()
        return Response(status=204)


# handle bilan radiologique
@api_view(['POST' , 'GET' , 'PUT', 'DELETE'])
def bilan_Radiologique_detail(request , consultation_id):
    if request.method == 'POST':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        request.data['consultation'] = consultation.id
        serializer = BilanRadiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_Radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            raise NotFound("Aucun bilan radiologique n'existe pour cette consultation")
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        serializer = BilanRadiologiqueSerializer(bilan_Radiologique)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan radiologique associé à cette consultation."}, status=404)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        request.data['consultation'] = consultation.id
        serializer = BilanRadiologiqueSerializer(bilan_radiologique, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan radiologique associé à cette consultation."}, status=404)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        bilan_radiologique.delete()
        return Response(status=204)
    



#handles examen biologique
@api_view(['POST' , 'GET'])
def examen_list(request , consultation_id):
    if request.method == 'POST':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        try:
            bilan = get_object_or_404(BilanBiologique, consultation=consultation)
        except Http404:
            return Response({"error": "Aucun bilan biologique n'existe pour cette consultation."}, status=404)
        serializer = ExamenBiologiqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bilan=bilan)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Http404:
            return Response({"error": "La consultation n'existe pas."}, status=404)
        try:
            bilan = get_object_or_404(BilanBiologique, consultation=consultation)
        except Http404:
            return Response({"error": "Aucun bilan biologique n'existe pour cette consultation."}, status=404)
        serializer = ExamenBiologiqueSerializer(bilan.examens , many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def examen_detail(request , examen_id):
    if request.method == 'GET':
        try:
            examen = get_object_or_404(ExamenBiologique, id=examen_id)
        except Http404:
            return Response({"error": "L'examen n'existe pas."}, status=404)
        serializer = ExamenBiologiqueSerializer(examen)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            examen = get_object_or_404(ExamenBiologique, id=examen_id)
        except Http404:
            return Response({"error": "L'examen n'existe pas."}, status=404)
        serializer = ExamenBiologiqueSerializer(examen, data=request.data , partial=True)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            examen = get_object_or_404(ExamenBiologique, id=examen_id)
        except Http404:
            return Response({"error": "L'examen n'existe pas."}, status=404)
        examen.delete()
        return Response(status=204)
    

@api_view(['GET'])
def ordonnance_list(request):
    if request.method == 'GET':
        serializers = OrdonnanceSerializer(Ordonnance.objects.all(), many=True)
        return Response(serializers.data)
    
@api_view(['put' , 'GET'])
def ordonnance_detail(request , ordonnance_id):
    if request.method == 'PUT':
        try:
            ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)
        except Http404:
            return Response({"error": "L'ordonnance n'existe pas."}, status=404)
        serializer = OrdonnanceSerializer(ordonnance, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)
        except Http404:
            return Response({"error": "L'ordonnance n'existe pas."}, status=404)
        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data)    
        
    