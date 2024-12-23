from rest_framework import serializers
from .models import DPI , BilanBiologique , Consultation , BilanRadiologique

class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['patient', 'medecin_traitant', 'nss', 'date_naissance', 'adresse', 'telephone', 'mutuelle', 'personne_a_contacter']


class BilanBiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanBiologique
        fields = ['consultation', 'date_bilan', 'comment']

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['dpi', 'date_consultation', 'motif']

class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanRadiologique
        fields = ['consultation', 'date_bilan', 'image', 'comment']
        