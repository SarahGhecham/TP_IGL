import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Patient, DPI, Consultation, Medecin


@pytest.mark.django_db
def test_patch_consultation_resume():
    # Create a user, patient, and medecin
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")
    
    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    # Create a DPI
    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789",
    )

    # Create a Consultation
    consultation = Consultation.objects.create(
        dpi=dpi,
        motif="Checkup",
        resume={"antecedents_medicaux": ["Asthma"], "observations_cliniques": "Stable"},
    )

    # Initialize API client
    client = APIClient()

    # Prepare patch data
    patch_data = {
        "resume": {
            "antecedents_medicaux": ["Hypertensions", "Diabète de type 2"],
            "observations_cliniques": "Patient présente des signes d'amélioration générale.",
            "diagnostic": "Amélioration notable avec traitement.",
        }
    }

    # Send patch request
    url = f"/dpi/consultation/{consultation.id}/resume/"
    response = client.patch(url, data=patch_data, format="json")

    # Assert the response status code and content
    assert response.status_code == status.HTTP_200_OK
    assert response.data["resume"]["antecedents_medicaux"] == ["Hypertensions", "Diabète de type 2"]
    assert response.data["resume"]["observations_cliniques"] == "Patient présente des signes d'amélioration générale."
    assert response.data["resume"]["diagnostic"] == "Amélioration notable avec traitement."

    # Verify the database was updated
    consultation.refresh_from_db()
    assert consultation.resume == patch_data["resume"]
