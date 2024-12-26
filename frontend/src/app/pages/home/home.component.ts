import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card'
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { MatIconModule } from '@angular/material/icon';
import { CalendarComponent } from '../../calendar/calendar.component';


@Component({
  selector: 'app-home',
  imports: [MatCardModule,NavbarComponent,MatIconModule,CalendarComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
