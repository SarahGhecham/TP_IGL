from django.urls import path
from .views import *
urlpatterns = [
    path('consultation/create/', CreateConsultationView.as_view(), name='create-consultation'),
    path('consultations/', ConsultationListView.as_view(), name='consultation-list'),
    path('consultations/<int:id>/delete/', DeleteConsultationView.as_view(), name='delete-consultation'),
    path('consultation/<int:pk>/resume/', ConsultationResumeView.as_view(), name='consultation-resume'),
    path('soins/', SoinListView.as_view(), name='soin-list'),
    path('soin/create/', SoinCreateView.as_view(), name='soin-create'),
    path('soin/<int:id>/', SoinDetailView.as_view(), name='soin-detail'),
    path('soins/delete/<int:id>/', SoinDetailView.as_view(), name='soin-delete'),
    path('resultats/', ResultatExamenImagerieListView.as_view(), name='resultat-list'),
    path('resultats/create/', ResultatExamenImagerieCreateView.as_view(), name='resultat-create'),
    path('resultats/<int:resultat_examen_id>/compte-rendu/create/', CompteRenduCreateView.as_view(), name='compte-rendu-create'),
    path('resultats/<int:pk>/update/', ResultatExamenImagerieUpdateView.as_view(), name='resultat-update'),
    path('compte-rendu/<int:pk>/update/', CompteRenduUpdateView.as_view(), name='compte-rendu-update'),
    path('resultats/<int:pk>/delete/', ResultatExamenImagerieDeleteView.as_view(), name='resultat-delete'),
    path('resultats/<int:id>/', ResultatExamenImagerieDetailView.as_view(), name='resultat-examen-imagerie-detail'),
    path('consultation/<int:consultation_id>/bilanRadiologique/', bilan_Radiologique_detail, name='bilan_radiologique_detail'),
    path('bilanRadiologique/', bilan_Radiologique_list, name='bilan_radiologique_list'),
    path('consultation/bilanBiologique/<int:bilan_id>/examen/', examen_list, name='examen_list'),
]
