import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AddConsultationComponent } from '../add-consultation/add-consultation.component';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { ConsultationService } from '../../services/consultation.service';

@Component({
  selector: 'app-consultations',
  imports: [RouterLink, CommonModule, FormsModule, AddConsultationComponent,NavbarComponent],
  templateUrl: './consultations.component.html',
  styleUrl: './consultations.component.scss'
})
export class ConsultationsComponent implements OnInit {
  consultations: any[] = []; // Tableau pour stocker les consultations
  showMotif: boolean = false; // Propriété pour contrôler l'affichage
  showAddConsultation: boolean = false; // Propriété pour contrôler l'affichage
  dpiId: string | null = null;
  nss: string | null = null;

  constructor(private route: ActivatedRoute,
    private consultationService: ConsultationService) {}

  ngOnInit() {
    const params = this.route.snapshot.queryParams;
    this.dpiId = params['id'];
    this.nss = params['nss'];

    // Charger les consultations si NSS est défini
    if (this.nss) {
      this.loadConsultations();
    }
  }

  loadConsultations(): void {
    this.consultationService.getAllConsultations(this.nss!).subscribe({
      next: (data) => (this.consultations = data),
      error: (err) => console.error('Erreur lors du chargement des consultations', err),
    });
  }

  toggleMotif(): void {
    this.showMotif = !this.showMotif; // Inverse l'état d'affichage
  }

  showPopUp(): void {
    this.showAddConsultation = true; // Inverse l'état d'affichage
  }

  // Fermer la popup si on clique en dehors
  closePopup(event: MouseEvent): void {
    this.showAddConsultation = false;
  }

  preventClose(event: MouseEvent): void {
    event.stopPropagation();
  }

  handleConsultationAdded(): void {
    this.showAddConsultation = false; // Fermer la popup
    this.loadConsultations(); // Actualiser la liste des consultations
  }
}
