import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { AddBilanradiologiqueComponent } from '../../components/add-bilanradiologique/add-bilanradiologique.component';
import { BilanRadiologiqueService } from '../../services/bilan-radiologique.service';

@Component({
  selector: 'app-bilan-radiologique',
  imports: [AddBilanradiologiqueComponent, CommonModule],
  templateUrl: './bilan-radiologique.component.html',
  styleUrl: './bilan-radiologique.component.scss'
})
export class BilanRadiologiqueComponent implements OnInit, OnChanges {
  @Input() Date: any; // La date reçue en entrée (peut être une chaîne ou un objet Date)
  @Input() nss!: string; // Le numéro de sécurité sociale du patient
  bilan: any; // Variable pour stocker le bilan radiologique
  isSameDay: boolean = false; // Variable pour stocker le résultat de la comparaison
  existBilan: boolean = false; // Variable pour stocker le résultat de la comparaison
  showAddBilanRadiologique: boolean = false;

  constructor(private bilanService: BilanRadiologiqueService) {}

  ngOnInit(): void {
    this.getBilanRadiologique();
  }

  showPopUp(): void {
    this.showAddBilanRadiologique = true; // Inverse l'état d'affichage
  }

  // Fermer la popup si on clique en dehors
  closePopup(event: MouseEvent): void {
    this.showAddBilanRadiologique = false;
  }

  preventClose(event: MouseEvent): void {
    event.stopPropagation();
  }

  ngOnChanges(): void {
    this.compareDates();
  }

  compareDates(): void {
    if (this.Date) {
      // Convertir la date reçue en objet Date (si nécessaire)
      const inputDate = new Date(this.Date);
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

  // Récupérer le bilan pour la date donnée
  getBilanRadiologique(): void {
    this.bilanService.getBilanByNss(this.nss).subscribe(
      (response: any) => {
        this.bilan = response;
        this.existBilan = !!response;
        this.compareDates();
      },
      (error) => {
        console.error('Erreur lors de la récupération du bilan:', error);
        this.existBilan = false;
      }
    );
  }
}
