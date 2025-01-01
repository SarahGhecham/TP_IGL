import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { AddConsultationService } from '../../services/add-consultation.service';

@Component({
  selector: 'app-add-consultation',
  imports: [FormsModule, CommonModule, RouterLink],
  templateUrl: './add-consultation.component.html',
  styleUrl: './add-consultation.component.scss'
})
export class AddConsultationComponent{
  // Données pour la consultation
  consultation = {
    date: '',
    motif: '',
  };
  constructor() {}


  // Ajouter la consultation (enregistrer ou envoyer au backend)
  addConsultation() {
    console.log('Consultation ajoutée :', this.consultation);
    // Ajouter la logique pour enregistrer la consultation
  }
}
