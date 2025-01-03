import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { AddBilanbiologiqueComponent } from '../../components/add-bilanbiologique/add-bilanbiologique.component';
import { AddExamenbiologiqueComponent } from '../../components/add-examenbiologique/add-examenbiologique.component';
import { Examen } from '../../models/examen';
import { ExamenService } from '../../services/examen.service';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-bilan-biologique',
  imports: [CommonModule,AddBilanbiologiqueComponent,AddExamenbiologiqueComponent, NavbarComponent],
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
  consultationId: number = 0;

  examens: any[] = [];

  constructor(private examenService: ExamenService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.consultationId = Number(this.route.snapshot.paramMap.get('id'));
    this.fetchBilan();
  }

  fetchBilan(): void {
    this.examenService.getBilanBiologique(this.consultationId).subscribe({
      next: (bilan) => {
        this.bilanDate = new Date(bilan.date_bilan);
        this.existBilan = true;
        this.compareDates();
        this.fetchExamens(); // Charger les examens associés
      },
      error: () => {
        this.existBilan = false;
      },
    });
  }

  fetchExamens(): void {
    this.examenService.getExamens(this.consultationId).subscribe({
      next: (data: any[]) => {
        // Mapper les données reçues pour s'assurer qu'elles sont compatibles avec l'affichage
        this.examens = data.map((examen) => ({
          type_examen: examen.type_examen,
          resultat: examen.resultat || null, // Null par défaut si pas de résultat
          unite: examen.unite || null,      // Null par défaut si pas d'unité
          date_examen: examen.date_examen,  // Si besoin pour le suivi
        }));
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

  handleBilanAdded(): void {
    this.createBilan();
    this.showBilan = false; // Fermer la popup
  }
  
  createBilan(): void {
    this.examenService.createBilanBiologique(this.consultationId).subscribe({
      next: (bilan) => {
        this.bilanDate = new Date(bilan.date_bilan);
        this.existBilan = true;
        this.compareDates();
      },
      error: (err) => {
        console.error('Erreur lors de la création du bilan biologique :', err);
      }
    });
  }

  addExamen(): void {
    const nouvelExamen = { type_examen: this.nomexamen };
    this.examenService.addExamen(this.consultationId, nouvelExamen).subscribe({
      next: (examen) => {
        this.examens.push(examen);
        this.showExamen = false; // Fermer la popup
      },
      error: (err) => {
        console.error('Erreur lors de l\'ajout de l\'examen :', err);
      },
    });
  }
}
