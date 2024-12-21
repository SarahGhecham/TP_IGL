from rest_framework import serializers
from .models import DPI

class DPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['patient', 'medecin_traitant', 'nss', 'date_naissance', 'adresse', 'telephone', 'mutuelle', 'personne_a_contacter']