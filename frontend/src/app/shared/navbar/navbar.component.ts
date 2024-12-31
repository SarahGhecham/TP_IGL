import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  isLoggedIn: boolean = false; 

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.isLoggedIn = this.authService.isLoggedIn(); // Check login status on component initialization
  }

  onLogout() {
    this.authService.logout(); // Log out the user
    this.isLoggedIn = false; // Update login status after logout
    console.log('User logged in:', this.isLoggedIn); // Log status to the console
  }
}
