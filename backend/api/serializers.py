from rest_framework import serializers
from .models import *

class DPISerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    class Meta:
        model = DPI
        fields = ['id', 'patient', 'medecin_traitant', 'nss', 'date_naissance', 'adresse', 'telephone', 'mutuelle', 'personne_a_contacter']


class BilanBiologiqueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    class Meta:
        model = BilanBiologique
        fields = ['id', 'consultation', 'date_bilan', 'comment']

class ConsultationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    dpi_id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    class Meta:
        model = Consultation
        fields = ['id','dpi_id', 'date_consultation', 'motif']

class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    class Meta:
        model = BilanRadiologique
        fields = ['id', 'consultation', 'date_bilan', 'image', 'comment']

class ExamenBiologiqueSerializer(serializers.ModelSerializer):
    bilan = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    class Meta:
        model = ExamenBiologique
        fields = ['id','bilan' ,'type_examen', 'resultat', 'unite', 'date_examen']
        