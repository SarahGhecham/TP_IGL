from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

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
    # patient = UserSerializer(read_only=True)
    # medecin_traitant = UserSerializer(read_only=True)
    class Meta:
        model = DPI
        fields = ['id', 'patient', 'medecin_traitant', 'nss', 'date_naissance', 'adresse', 'telephone', 'mutuelle', 'personne_a_contacter']



class ConsultationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only
    dpi = DPISerializer(read_only=True)
    class Meta:
        model = Consultation
        fields = ['id','dpi', 'date_consultation', 'motif', 'resume']

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
    id = serializers.PrimaryKeyRelatedField(read_only=True)  
    consultation = ConsultationSerializer(read_only=True)
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
