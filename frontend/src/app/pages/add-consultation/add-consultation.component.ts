import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { AddConsultationService } from '../../services/add-consultation.service';

@Component({
  selector: 'app-add-consultation',
  imports: [FormsModule, CommonModule],
  templateUrl: './add-consultation.component.html',
  styleUrl: './add-consultation.component.scss'
})
export class AddConsultationComponent {
  @Output() consultationAdded = new EventEmitter<void>();

  consultation = {
    date: '',
    motif: '',
  };

  constructor(private addConsultationService: AddConsultationService, private router: Router) {}

  addConsultation() {
    this.addConsultationService.createConsultation(this.consultation).subscribe({
      next: () => {
        console.log('Consultation ajoutée avec succès');
        this.consultationAdded.emit(); // Notifier le parent
      },
      error: (err) => console.error('Erreur lors de l’ajout de la consultation :', err),
    });
  }
}
