from rest_framework import serializers
from api.models import Consultation,Soin,ResultatExamenImagerie,CompteRendu,DPI,Infirmier


class SoinSerializer(serializers.ModelSerializer):
    dpi = serializers.PrimaryKeyRelatedField(queryset=DPI.objects.all()) 
    infirmier = serializers.PrimaryKeyRelatedField(queryset=Infirmier.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Soin
        fields = ['id', 'dpi', 'infirmier', 'description', 'date_soin', 'observations']



class ResumeSerializer(serializers.Serializer):
    antecedents_medicaux = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    observations_cliniques = serializers.CharField(required=False)
    diagnostic = serializers.CharField(required=False)


class ConsultationSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(required=False) 
    class Meta:
        model = Consultation
        fields = ['id', 'dpi', 'date_consultation', 'motif', 'resume']

class CompteRenduSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = CompteRendu
        fields = ['texte', 'date_creation']

class ResultatExamenImagerieSerializerForGet(serializers.ModelSerializer):
    compte_rendu = CompteRenduSerializerForGet(read_only=True)  # Le compte-rendu est un champ de lecture seule

    class Meta:
        model = ResultatExamenImagerie
        fields = ['dpi', 'radiologue', 'image', 'commentaire', 'date_examen', 'compte_rendu']


class ResultatExamenImagerieSerializer(serializers.ModelSerializer):
    dpi = serializers.PrimaryKeyRelatedField(queryset=DPI.objects.all())  
    radiologue = serializers.StringRelatedField() 
    compte_rendu = serializers.StringRelatedField() 

    class Meta:
        model = ResultatExamenImagerie
        fields = ['id', 'dpi', 'radiologue', 'image', 'commentaire', 'date_examen', 'compte_rendu']


class CompteRenduSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteRendu
        fields = ['id', 'texte', 'date_creation']

