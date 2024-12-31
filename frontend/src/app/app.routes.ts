import { LoginComponent } from './pages/auth/login/login.component';
import { Routes } from '@angular/router';
import { HomeMedComponent } from './pages/users/medecin/home/home.component';
import { ExamenTrendsComponent } from './pages/examen-trend/examen-trend.component';
import { HomeComponent } from './pages/home/home.component';
import { AcceuilAdComponent } from './pages/users/administratif/acceuil/acceuilAd.component';
import { CreateDPIComponent } from './pages/users/administratif/create-dpi/create-dpi.component';
import { OrdonnanceComponent } from './pages/users/medecin/ordonnance/ordonnance.component';
import { AuthGuard } from './guards/auth.guard';

import { InfirmierComponent } from './pages/users/infirmier/infirmier.component';
import { LaborantinComponent } from './pages/users/laborantin/laborantin.component';
import { RadiologueComponent } from './pages/users/radiologue/radiologue.component';


export const routes: Routes = [
  // Public Routes
  { path: 'login', component: LoginComponent }, // Route for the login page
  { path: '', component: HomeComponent }, // Route for the home page

  // Administratif Routes (Role: administratif)
  {
    path: 'users/administratif',
    canActivate: [AuthGuard],
    children: [
      { path: '', component: AcceuilAdComponent }, // Default administratif page
      { path: 'create-dpi', component: CreateDPIComponent }, // Create DPI page
    ]
  },

  // Medecin Routes (Role: medecin)
  {
    path: 'users/medecin',
    canActivate: [AuthGuard],
    children: [
      { path: '', component: HomeMedComponent }, // Default medecin page
      { path: 'examen-trends', component: ExamenTrendsComponent }, // Examen trends page
      {path: 'ordonnance', component: OrdonnanceComponent}
    ]

  },  {
    path: 'users/infirmier',
    canActivate: [AuthGuard],
    children: [
      { path: '', component: InfirmierComponent }, // Default medecin page
      { path: 'examen-trends', component: ExamenTrendsComponent }, // Examen trends page
      {path: 'ordonnance', component: OrdonnanceComponent}
    ]
  },
  {
    path: 'users/laborantin',
    canActivate: [AuthGuard],
    children: [
      { path: '', component: LaborantinComponent }, // Default medecin page
      { path: 'examen-trends', component: ExamenTrendsComponent }, // Examen trends page
      {path: 'ordonnance', component: OrdonnanceComponent}
    ]
  },
  {
    path: 'users/radiologue',
    canActivate: [AuthGuard],
    children: [
      { path: '', component: RadiologueComponent }, // Default medecin page
      { path: 'examen-trends', component: ExamenTrendsComponent }, // Examen trends page
      {path: 'ordonnance', component: OrdonnanceComponent}
    ]
  },

  },

  // Wildcard Route (Redirect to Login)
  { path: '**', redirectTo: 'login' }
];
