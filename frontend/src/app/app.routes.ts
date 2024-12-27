import { LoginComponent } from './pages/auth/login/login.component';
import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AcceuilAdComponent } from './pages/users/administratif/acceuil/acceuilAd.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent }, // Route for the login page
  { path: '', component: HomeComponent },   // Route for the home page
  { path: 'users/administratif', component: AcceuilAdComponent },   // Route for the administratif acceuil page
  { path: '**', redirectTo: 'login' }          // Wildcard route redirects to login
];