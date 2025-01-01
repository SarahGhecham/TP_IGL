import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-affichetype',
  imports: [],
  templateUrl: './affichetype.component.html',
  styleUrl: './affichetype.component.scss'
})
export class AffichetypeComponent {
  @Input() type!: string;
}
