import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../../shared/navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { CalendarComponent } from './components/calendar/calendar.component';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../../services/auth.service';

@Component({
  selector: 'app-acceuil',
  imports: [NavbarComponent,CommonModule, CalendarComponent, RouterModule],
  templateUrl: './acceuilAd.component.html',
  styleUrl: './acceuilAd.component.scss'
})

export class AcceuilAdComponent implements OnInit {
  administratifName: string = ''; 

   constructor(private router: Router, private authService: AuthService) {}

   ngOnInit(): void {
    this.getDoctorName();
  }

  getDoctorName(): void {
    // Get the username from the token
    const username = this.authService.getUsername();
    if (username) {
      this.administratifName = username.toUpperCase(); 
    } 
  }
  onClick(){
    this.router.navigate(['/users/administratif/create-dpi']);
  }
}