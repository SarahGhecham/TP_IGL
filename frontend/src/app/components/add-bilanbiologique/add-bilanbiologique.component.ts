import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-bilanbiologique',
  imports: [CommonModule, FormsModule],
  templateUrl: './add-bilanbiologique.component.html',
  styleUrl: './add-bilanbiologique.component.scss'
})
export class AddBilanbiologiqueComponent {
  @Output() bilanAdded = new EventEmitter<Date>();
  bilanDate: string = '';

  submitBilan(): void {
    if (this.bilanDate) {
      this.bilanAdded.emit(new Date(this.bilanDate));
    }
  }
}
