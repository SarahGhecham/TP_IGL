from django.core.management.base import BaseCommand
from api.models import Patient, DPI, Medecin
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):
    help = 'Peuple la base de données avec des DPI, des patients et des médecins'

    def handle(self, *args, **kwargs):
        # Créer un utilisateur pour le patient
        patient_user = User.objects.create_user(username="patient1", password="securepassword", first_name="John", last_name="Doe")

        # Créer un patient
        patient = Patient.objects.create(user=patient_user)

        # Créer un médecin
        medecin_user = User.objects.create_user(username="medecin1", password="securepassword1",first_name="Dr. Alice", last_name="Smith")
        medecin = Medecin.objects.create(user=medecin_user)
        # Créer un DPI
        dpi = DPI.objects.create(
            patient=patient,
            nss="123-45-6789",
            date_naissance=date(1985, 5, 15),
            adresse="123 rue Exemple, Paris",
            telephone="0123456789",
            mutuelle="Mutuelle A",
            personne_a_contacter="Marie Doe"
        )

        # Lier le médecin traitant au DPI
        dpi.medecin_traitant = medecin
        dpi.save()

        

        self.stdout.write(self.style.SUCCESS('Base de données peuplée avec succès'))
