import { Routes } from '@angular/router';
import { HomeComponent } from './pages/users/medecin/home/home.component';
import { ExamenTrendsComponent } from './pages/examen-trend/examen-trend.component';

//import { SignInComponent } from './pages/sign-in/sign-in.component';
export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  /*{path:'signIn',
    component:SignInComponent,
  },*/
];
