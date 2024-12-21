from django.core.management.base import BaseCommand
from api.models import Patient, DPI, Medecin , Consultation, BilanBiologique, ExamenBiologique
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = 'Peuple la base de données avec des exemples de DPI, consultations, bilans et examens'

    def handle(self, *args, **kwargs):
        # Assurez-vous que le DPI d'ID 1 existe dans la base de données
        try:
            dpi = DPI.objects.get(id=1)
        except DPI.DoesNotExist:
            self.stdout.write(self.style.ERROR("Le DPI avec l'ID 1 n'existe pas."))
            return

        # Créer une consultation pour ce DPI
        consultation_1 = Consultation.objects.create(
            dpi=dpi,
            date_consultation=datetime(2024, 12, 21, 14, 30),
            motif="Suivi médical de routine"
        )
        self.stdout.write(self.style.SUCCESS(f"Consultation créée : {consultation_1}"))

        # Créer un bilan biologique pour la consultation
        bilan_1 = BilanBiologique.objects.create(
            consultation=consultation_1,
        )
        self.stdout.write(self.style.SUCCESS(f"Bilan biologique créé : {bilan_1}"))

        # Créer des examens biologiques pour le bilan
        examen_1 = ExamenBiologique.objects.create(
            bilan=bilan_1,
            type_examen="Glycemie",
            resultat=100.0,  # Exemple de résultat (en mg/dl)
            unite="mg/dl",
            date_examen=datetime(2024, 12, 22, 15, 30)
        )
        self.stdout.write(self.style.SUCCESS(f"Examen de glycémie créé : {examen_1}"))
        examen_2 = ExamenBiologique.objects.create(
            bilan=bilan_1,
            type_examen="Glycemie",
            resultat=120.0,  # Exemple de résultat (en mg/dl)
            unite="mg/dl",
            date_examen=datetime(2024, 12, 25, 15, 30)
        )
        self.stdout.write(self.style.SUCCESS(f"Examen de glycémie créé : {examen_2}"))

        examen_3 = ExamenBiologique.objects.create(
            bilan=bilan_1,
            type_examen="Cholesterol",
            resultat=190.0,  # Exemple de résultat (en mg/dl)
            unite="mg/dl",
            date_examen=datetime(2024, 12, 21, 15, 30)
        )
        self.stdout.write(self.style.SUCCESS(f"Examen de cholestérol créé : {examen_3}"))

        # Vous pouvez ajouter plus de données ou créer des structures similaires si nécessaire.
        self.stdout.write(self.style.SUCCESS('Base de données peuplée avec succès!'))
    '''
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
        '''
