from django.core.management.base import BaseCommand
from api.models import Patient, DPI, Medecin, Consultation, BilanBiologique, ExamenBiologique
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):
    help = 'Peupler la base de données avec un patient et un DPI'

    def handle(self, *args, **kwargs):
        try:
            # Récupérer un médecin existant dans la base de données
            user1 = User.objects.get(username="new_medecin")
            medecin = Medecin.objects.get(user=user1)

            # Récupérer un patient existant
            user = User.objects.get(username="john_doe")
            patient = Patient.objects.get(user=user)

            # Créer un DPI pour ce patient et en associant un médecin traitant existant
            dpi = DPI.objects.create(
                patient=patient,
                medecin_traitant=medecin,  # Utilisation du médecin existant
                nss="123456789012345",
                date_naissance=date(2004, 12, 11),  # Utilisation du type date correct
                adresse="123 rue de Paris",
                telephone="0123456789",
                mutuelle="Mutuelle Santé",
                personne_a_contacter="Marie Dupont"
            )

            # Afficher un message de confirmation
            self.stdout.write(self.style.SUCCESS(f"DPI créé: {dpi}"))

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("Utilisateur non trouvé."))
        except Medecin.DoesNotExist:
            self.stdout.write(self.style.ERROR("Médecin non trouvé."))
        except Patient.DoesNotExist:
            self.stdout.write(self.style.ERROR("Patient non trouvé."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Une erreur est survenue : {e}"))
