import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

@Component({
  selector: 'app-main-consultdpi',
  imports: [RouterLink,NavbarComponent],
  templateUrl: './main-consultdpi.component.html',
  styleUrl: './main-consultdpi.component.scss'
})
export class MainConsultdpiComponent {
  
}
