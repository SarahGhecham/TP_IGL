import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Consultation, BilanRadiologique, ResultatExamenImagerie, DPI, Medecin, Patient, Infirmier, Radiologue
from django.contrib.auth.models import User
from django.utils import timezone
from unittest.mock import MagicMock

@pytest.mark.django_db
def test_get_bilan_radiologique():
    # Reuse setup from the previous test
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    consultation = Consultation.objects.create(
        dpi=dpi,
        motif="Checkup",
        resume={"note": "First consultation"}
    )

    bilan = BilanRadiologique.objects.create(
        consultation=consultation,
        comment="All good"
    )

    # Create API client and make the GET request
    client = APIClient()
    response = client.get(f'/dpi/consultation/{consultation.id}/bilanRadiologique/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['consultation'] == consultation.id
    assert 'resultats' in response.data

@pytest.mark.django_db
def test_get_bilan_radiologique_list():
    # Reuse setup from the previous tests
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    consultation = Consultation.objects.create(
        dpi=dpi,
        motif="Checkup",
        resume={"note": "First consultation"}
    )

    BilanRadiologique.objects.create(
        consultation=consultation,
        comment="All good"
    )

    # Create API client and make the GET request to get all bilans
    client = APIClient()
    response = client.get('/dpi/bilanRadiologique/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_get_examen_list():
    # Reuse setup from previous tests
    medecin_user = User.objects.create_user(username="medecin1", password="password123")
    medecin = Medecin.objects.create(user=medecin_user, specialite="Cardiologie")

    patient_user = User.objects.create_user(username="patient1", password="password123")
    patient = Patient.objects.create(user=patient_user, adresse="123 Rue Example", telephone="123456789")

    dpi = DPI.objects.create(
        patient=patient,
        medecin_traitant=medecin,
        nss="123456789012345",
        date_naissance="1990-01-01",
        adresse="123 Rue Example",
        telephone="123456789"
    )

    consultation = Consultation.objects.create(
        dpi=dpi,
        motif="Checkup",
        resume={"note": "First consultation"}
    )

    bilan = BilanRadiologique.objects.create(
        consultation=consultation,
        comment="All good"
    )

    radiologue_user = User.objects.create_user(username="radiologue1", password="password123")
    radiologue = Radiologue.objects.create(user=radiologue_user)

    resultat = ResultatExamenImagerie.objects.create(
        radiologue=radiologue,
        commentaire="No issues",
        date_examen=timezone.now()
    )
    bilan.resultats.add(resultat)

    # Create API client and make the GET request to fetch resultats
    client = APIClient()
    response = client.get(f'/dpi/consultation/bilanBiologique/{bilan.id}/examen/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

