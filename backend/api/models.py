from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire, comme spécialité, etc.
    def __str__(self):
        return self.user.get_full_name()

class Infirmier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.get_full_name()

class Laborantin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.get_full_name()

class Radiologue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.get_full_name()

class Administratif(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.get_full_name()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relation avec la classe User
    # Vous pouvez ajouter des méthodes ou des propriétés spécifiques à Patient ici
    @property
    def nom(self):
        return self.user.last_name

    @property
    def prenom(self):
        return self.user.first_name

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
        return f"DPI de {self.patient.user.get_full_name()}"
