from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

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
        fields = ['id','dpi_id', 'date_consultation', 'motif', 'resume']

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

class OrdonnanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordonnance
        fields = ['id', 'consultation', 'date_ordonnance', 'text' , 'valid']
        

class RoleSignupSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[
        ('medecin', 'Médecin'),
        ('infirmier', 'Infirmier'),
        ('laborantin', 'Laborantin'),
        ('radiologue', 'Radiologue'),
        ('administratif', 'Administratif'),
        ('patient', 'Patient')
    ])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)

        # Assign the user to the corresponding role model
        if role == 'medecin':
            Medecin.objects.create(user=user)
        elif role == 'infirmier':
            Infirmier.objects.create(user=user)
        elif role == 'laborantin':
            Laborantin.objects.create(user=user)
        elif role == 'radiologue':
            Radiologue.objects.create(user=user)
        elif role == 'administratif':
            Administratif.objects.create(user=user)
        elif role == 'patient':
            Patient.objects.create(user=user)

        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):       
     def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username  
        return data
