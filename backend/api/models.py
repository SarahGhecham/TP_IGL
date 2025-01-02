from django.db import models
from django.contrib.auth.models import User

# Médecin
class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.username} "

# Infirmier
class Infirmier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.username

# Radiologue
class Radiologue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Laborantin
class Laborantin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Administratif(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ajoutez d'autres champs si nécessaire.
    def __str__(self):
        return self.user.username
    
class Pharmacien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    @property
    def nom(self):
        return self.user.last_name

    @property
    def prenom(self):
        return self.user.first_name

    def __str__(self):
        return self.user.username
    
class DPI(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, related_name="patients")
    nss = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    mutuelle = models.CharField(max_length=100, blank=True, null=True)
    personne_a_contacter = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"DPI de {self.patient.user.username}"
    

class Consultation(models.Model):
    dpi = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='consultations')
    date_consultation = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(max_length=255)
    resume = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Consultation du {self.date_consultation} pour {self.dpi}"
    

class Ordonnance(models.Model):
    consultation = models.OneToOneField(Consultation , on_delete=models.CASCADE,related_name='ordonnance')
    date_ordonnance = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True , null=True)
    valid = models.BooleanField(default=False)

    def __str__(self):
        return f"Ordonnance pour {self.consultation}"
    

class BilanBiologique(models.Model):
    consultation = models.OneToOneField(Consultation , on_delete=models.CASCADE,related_name='bilanBiologique')
    date_bilan = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Bilan pour {self.consultation}"

    
class ExamenBiologique(models.Model):
    bilan = models.ForeignKey(BilanBiologique, on_delete=models.CASCADE, related_name='examens')
    type_examen = models.CharField(max_length=255)
    resultat = models.FloatField(blank=True , null=True)  
    unite = models.CharField(max_length=50 , blank=True , null=True)  
    date_examen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Examen {self.type_examen} pour {self.bilan.consultation}"
    
# Soin
class Soin(models.Model):
    dpi = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='soins')
    infirmier = models.ForeignKey(Infirmier, on_delete=models.SET_NULL, null=True, related_name='soins')
    description = models.TextField()
    date_soin = models.DateTimeField(auto_now_add=True)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Soin par {self.infirmier} le {self.date_soin}"


class BilanRadiologique(models.Model):
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='bilanRadiologique'
    )
    date_bilan = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    resultats = models.ManyToManyField(
        'ResultatExamenImagerie',
        related_name='bilans',
        blank=True
    )

    def __str__(self):
        return f"Bilan du {self.date_bilan} pour {self.consultation}"

class ResultatExamenImagerie(models.Model):
    radiologue = models.ForeignKey(
        Radiologue,
        on_delete=models.SET_NULL,
        null=True,
        related_name='resultats_imagerie'
    )
    image = models.ImageField(upload_to='imagerie/%Y/%m/%d/', blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    date_examen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Examen d'imagerie pour {self.radiologue}"

    def has_compte_rendu(self):
        return hasattr(self, 'compte_rendu')

class CompteRendu(models.Model):
    resultat_examen = models.OneToOneField(
        ResultatExamenImagerie,
        on_delete=models.CASCADE,
        related_name='compte_rendu',
    )
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['resultat_examen'], 
                name='unique_compte_rendu_per_resultat'
            )
        ]

    def __str__(self):
        return f"Compte Rendu pour {self.resultat_examen.radiologue}"

# Résultat d'analyse biologique
class ResultatAnalyseBiologique(models.Model):
    dpi = models.ForeignKey(DPI, on_delete=models.CASCADE, related_name='resultats_biologiques')
    laborantin = models.ForeignKey(Laborantin, on_delete=models.SET_NULL, null=True, related_name='analyses_biologiques')
    type_analyse = models.CharField(max_length=255)
    resultat = models.CharField(max_length=255)
    unite = models.CharField(max_length=50, blank=True, null=True)
    date_analyse = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analyse biologique ({self.type_analyse}) par {self.laborantin} pour {self.dpi.patient.user.get_full_name()}"

