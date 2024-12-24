from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire, comme spécialité, etc.
    def __str__(self):
        return f"Dr. {self.user.username} "

class Infirmier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.username

class Laborantin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.username

class Radiologue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.username

class Administratif(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  

    @property
    def nom(self):
        return self.user.last_name

    @property
    def prenom(self):
        return self.user.first_name
    
    def __str__(self):
        return f"Patient {self.user.username}"

class DPI(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)  # Relation OneToOne avec Patient
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, related_name="patients")
    nss = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    mutuelle = models.CharField(max_length=100)
    personne_a_contacter = models.CharField(max_length=100)

    def __str__(self):
        return f"DPI de nss {self.nss}"


class Consultation(models.Model):
    dpi = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='consultations')
    date_consultation = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(max_length=255)
    resume = models.TextField(blank=True , null=True)

    def __str__(self):
        return f"Consultation du id {self.id}"
    

class BilanBiologique(models.Model):
    consultation = models.OneToOneField(Consultation , on_delete=models.CASCADE,related_name='bilanBiologique')
    date_bilan = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Bilan pour {self.consultation}"

class BilanRadiologique(models.Model):
    consultation = models.OneToOneField(Consultation , on_delete=models.CASCADE,related_name='bilanRadiologique')
    date_bilan = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/radiology/' , null=True , blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Bilan du {self.date_bilan} pour {self.consultation}"



class ExamenBiologique(models.Model):
    bilan = models.ForeignKey(BilanBiologique, on_delete=models.CASCADE, related_name='examens')
    type_examen = models.CharField(max_length=255)
    resultat = models.FloatField(blank=True , null=True)  
    unite = models.CharField(max_length=50 , blank=True , null=True)  
    date_examen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Examen {self.type_examen} pour {self.bilan.consultation}"
    

