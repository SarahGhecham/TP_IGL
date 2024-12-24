from django.shortcuts import render , get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from .serializers import *
from .models import *



@api_view(['GET'])
def DPI_list(request):
    if request.method == 'GET':
        serializers = DPISerializer(DPI.objects.all(), many=True)
        return Response(serializers.data)

@api_view(['GET'])
def DPI_detail(request , nss) :
    try:
        dpi = get_object_or_404(DPI , nss = nss)
    except Exception as e :
        raise NotFound ("Ce DPI n'existe pas")
    serializer = DPISerializer(dpi)
    return Response(serializer.data)


#handle consulation
@api_view(['POST' , 'GET'])
def consultation_list(request , nss):
    if request.method == 'POST':
        try:
            dpi = get_object_or_404(DPI, nss=nss)
        except Exception as e:
            raise NotFound("Vous n'avez pas encore de DPI")
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dpi=dpi)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    if request.method == 'GET':
        try:
            dpi = get_object_or_404(DPI, nss=nss)
        except Exception as e:
            raise NotFound("Vous n'avez pas encore de DPI")
        serializer = ConsultationSerializer(dpi.consultations , many=True)
        return Response(serializer.data)    

@api_view(['GET', 'PUT', 'DELETE'])
def consultation_detail(request , consultation_id):
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        serializer = ConsultationSerializer(consultation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        consultation.delete()
        return Response(status=204) 


#handle bilan biologique
@api_view(['POST' , 'GET' , 'PUT' , 'DELETE'])
def bilan_Bilologique_detail(request , consultation_id): 
    if request.method == 'POST':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
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
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        serializer = BilanBiologiqueSerializer(bilan_biologique )
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_biologique = consultation.bilanBiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan biologique associé à cette consultation."}, status=404)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
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
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        bilan_biologique.delete()
        return Response(status=204)


# handle bilan radiologique
@api_view(['POST' , 'GET' , 'PUT', 'DELETE'])
def bilan_Radiologique_detail(request , consultation_id):
    if request.method == 'POST':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
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
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        serializer = BilanRadiologiqueSerializer(bilan_Radiologique)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
            bilan_radiologique = consultation.bilanRadiologique
        except ObjectDoesNotExist:
            return Response({"error": "Aucun bilan radiologique associé à cette consultation."}, status=404)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
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
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        bilan_radiologique.delete()
        return Response(status=204)
    



#handles examen biologique
@api_view(['POST' , 'GET'])
def examen_list(request , consultation_id):
    if request.method == 'POST':
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
    if request.method == 'GET':
        try:
            consultation = get_object_or_404(Consultation, id=consultation_id)
        except Exception as e:
            raise NotFound("La consultation n'existe pas")
        try:
            bilan = get_object_or_404(BilanBiologique, consultation=consultation)
        except Exception as e:
            raise NotFound("Aucun bilan biologique n'existe pour cette consultation")
        serializer = ExamenBiologiqueSerializer(bilan.examens , many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def examen_detail(request , examen_id):
    if request.method == 'GET':
        try:
            examen = get_object_or_404(ExamenBiologique, id=examen_id)
        except Exception as e:
            raise NotFound("L'examen n'existe pas")
        serializer = ExamenBiologiqueSerializer(examen)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            examen = get_object_or_404(ExamenBiologique, id=examen_id)
        except Exception as e:
            raise NotFound("L'examen n'existe pas")
        serializer = ExamenBiologiqueSerializer(examen, data=request.data , partial=True)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            examen = get_object_or_404(ExamenBiologique, id=examen_id)
        except Exception as e:
            raise NotFound("L'examen n'existe pas")
        examen.delete()
        return Response(status=204)