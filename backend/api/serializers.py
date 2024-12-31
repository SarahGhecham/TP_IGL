from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
class DPISerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    patient = UserSerializer(read_only=True)
    medecin_traitant = UserSerializer(read_only=True)
    class Meta:
        model = DPI
        fields = ['id', 'patient', 'medecin_traitant', 'nss', 'date_naissance', 'adresse', 'telephone', 'mutuelle', 'personne_a_contacter']




class ConsultationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    dpi = DPISerializer(read_only=True)
    class Meta:
        model = Consultation
        fields = ['id','dpi', 'date_consultation', 'motif' , "resume"]
class BilanBiologiqueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    consultation = ConsultationSerializer(read_only=True)
    class Meta:
        model = BilanBiologique
        fields = ['id', 'consultation', 'date_bilan', 'comment']
class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    consultation = ConsultationSerializer(read_only=True)
    class Meta:
        model = BilanRadiologique
        fields = ['id', 'consultation', 'date_bilan', 'image', 'comment']

class ExamenBiologiqueSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    bilan = BilanBiologiqueSerializer(read_only=True)
    class Meta:
        model = ExamenBiologique
        fields = ['id','bilan' ,'type_examen', 'resultat', 'unite', 'date_examen']

class OrdonnanceSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    consultation = ConsultationSerializer(read_only=True)
    class Meta:
        model = Ordonnance
        fields = ['id', 'consultation', 'date_ordonnance', 'text' , 'valid']
        
