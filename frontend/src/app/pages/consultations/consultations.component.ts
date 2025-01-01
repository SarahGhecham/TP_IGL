import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AddConsultationComponent } from '../add-consultation/add-consultation.component';

@Component({
  selector: 'app-consultations',
  imports: [RouterLink, CommonModule, FormsModule, AddConsultationComponent],
  templateUrl: './consultations.component.html',
  styleUrl: './consultations.component.scss'
})
export class ConsultationsComponent implements OnInit {
  showMotif: boolean = false; // Propriété pour contrôler l'affichage
  showAddConsultation: boolean = false; // Propriété pour contrôler l'affichage
  constructor() {} // Pas de dépendance ici

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

  ngOnInit(): void {
    // Rien à faire ici
  }
}
