import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { AddBilanbiologiqueComponent } from '../../components/add-bilanbiologique/add-bilanbiologique.component';
import { AddExamenbiologiqueComponent } from '../../components/add-examenbiologique/add-examenbiologique.component';
import { Examen } from '../../models/examen';
import { ExamenService } from '../../services/examen.service';

@Component({
  selector: 'app-bilan-biologique',
  imports: [CommonModule,AddBilanbiologiqueComponent,AddExamenbiologiqueComponent],
  templateUrl: './bilan-biologique.component.html',
  styleUrl: './bilan-biologique.component.scss'
})
export class BilanBiologiqueComponent implements OnInit, OnChanges {
  nomexamen: string = '';
  bilanDate: Date = new Date(); // Date du bilan biologique
  isSameDay: boolean = false;
  existBilan: boolean = true;
  showBilan: boolean = false;
  showExamen: boolean = false;

  examens: Examen[] = [];

  constructor(private examenService: ExamenService) {}

  ngOnInit(): void {
    // this.fetchBilanDate(); // Récupération de la date du bilan biologique au chargement
  }

  // Récupérer la date du bilan biologique depuis le backend
  fetchBilanDate(): void {
    this.examenService.getBilanBiologique().subscribe({
      next: (date: Date) => {
        this.bilanDate = date; // Stocke la date reçue
        this.existBilan = true; // Marque le bilan comme existant
        this.compareDates(); // Vérifie si la date est aujourd'hui     
        this.fetchExamens(); // Récupération des examens au chargement
      },
      error: (err) => {
        console.error('Erreur lors de la récupération du bilan biologique:', err);
        this.existBilan = false;
      },
    });
  }

  fetchExamens(): void {
    this.examenService.getExamens().subscribe({
      next: (data) => {
        this.examens = data; // Stocker les examens reçus
      },
      error: (error) => {
        console.error('Erreur lors de la récupération des examens :', error);
      },
    });
  }

  showPopUpBilan(): void {
    this.showBilan = true; // Inverse l'état d'affichage
  }

  // Fermer la popup si on clique en dehors
  closePopupBilan(event: MouseEvent): void {
    this.showBilan = false;
  }

  showPopUpExamen(): void {
    this.showExamen = true; // Inverse l'état d'affichage
  }

  // Fermer la popup si on clique en dehors
  closePopupExamen(event: MouseEvent): void {
    this.showExamen = false;
  }
  
  preventClose(event: MouseEvent): void {
    event.stopPropagation();
  }
  ngOnChanges(): void {
    this.compareDates();
  }

  compareDates(): void {
    if (this.bilanDate) {
      // Convertir la date reçue en objet Date (si nécessaire)
      const inputDate = this.bilanDate
      const today = new Date();

      // Comparer les années, mois et jours
      this.isSameDay =
        inputDate.getFullYear() === today.getFullYear() &&
        inputDate.getMonth() === today.getMonth() &&
        inputDate.getDate() === today.getDate();

      console.log('La date reçue est-elle aujourd\'hui ? ', this.isSameDay);
    } else {
      console.warn('Aucune date reçue en entrée.');
    }
  }

  addExamen(): void {
    const nouvelExamen = new Examen(this.nomexamen, '', '/');
    this.examenService.addExamen(nouvelExamen).subscribe({
      next: (result) => {
        console.log('Examen ajouté avec succès :', result);
        this.examens.push(result); // Ajouter l'examen à la liste locale
      },
      error: (err) => {
        console.error('Erreur lors de l\'ajout de l\'examen :', err);
      }
    });

    this.showExamen = false; // Fermer la popup
  }
}
