import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-bilanradiologique',
  imports: [FormsModule],
  templateUrl: './add-bilanradiologique.component.html',
  styleUrl: './add-bilanradiologique.component.scss'
})
export class AddBilanradiologiqueComponent {
  @Input() nomBilan: string = ''; // Champ pour le nom du bilan
  @Input() dateBilan: string = ''; // Champ pour la date du bilan
  @Output() addBilan: EventEmitter<{ nom: string; date: string }> = new EventEmitter<{ nom: string; date: string }>();


  onAddBilan(): void {
    if (this.nomBilan.trim() && this.dateBilan) {
      // Émettre l'objet contenant le nom et la date
      this.addBilan.emit({
        nom: this.nomBilan.trim(),
        date: this.dateBilan,
      });
    }
  }  
}
