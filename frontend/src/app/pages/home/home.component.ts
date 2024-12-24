import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card'
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { MatIconModule } from '@angular/material/icon';



@Component({
  selector: 'app-home',
  imports: [MatCardModule,NavbarComponent,MatIconModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
