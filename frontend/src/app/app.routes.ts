import { LoginComponent } from './pages/auth/login/login.component';
import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AcceuilAdComponent } from './pages/users/administratif/acceuil/acceuilAd.component';
import { CreateDPIComponent } from './pages/users/administratif/create-dpi/create-dpi.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent }, // Route for the login page
  { path: '', component: HomeComponent },   // Route for the home page
  { path: 'users/administratif', component: AcceuilAdComponent, canActivate: [AuthGuard] }, 
    // Route for the administratif acceuil page
  { path: 'users/administratif/create-dpi', component: CreateDPIComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: 'login' }          // Wildcard route redirects to login
];