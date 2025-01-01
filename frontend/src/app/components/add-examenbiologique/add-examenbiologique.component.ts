import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-examenbiologique',
  imports: [FormsModule],
  templateUrl: './add-examenbiologique.component.html',
  styleUrl: './add-examenbiologique.component.scss'
})
export class AddExamenbiologiqueComponent {
  @Input() nomexamen: string = ''; // Nom initial de l'examen reçu du parent
  @Output() addExamen: EventEmitter<string> = new EventEmitter<string>(); // Correctement typé

  // Méthode pour émettre l'événement au parent
  onAddExamen(): void {
    this.addExamen.emit(this.nomexamen.trim());
  }
}
