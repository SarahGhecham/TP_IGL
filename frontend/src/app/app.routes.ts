import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LayoutComponent } from './pages/layout/layout.component';
import { MainConsultdpiComponent } from './pages/main-consultdpi/main-consultdpi.component';
import { ConsultationsComponent } from './pages/consultations/consultations.component';
import { ConsultationComponent } from './pages/consultation/consultation.component';
import { AddConsultationComponent } from './pages/add-consultation/add-consultation.component';
import { BilanComponent } from './pages/bilan/bilan.component';
import { OrdonanceComponent } from './pages/ordonance/ordonance.component';
//import { SignInComponent } from './pages/sign-in/sign-in.component';
export const routes: Routes = [
  {
    path: '',
    component: LayoutComponent,
    // canActivate: [AuthGuard],
    children: [
      {
        path: 'consultation-dpi', component: MainConsultdpiComponent ,
      },
      {
        path: 'consultations',
        children: [
          {
            path: '', component: ConsultationsComponent,
          },
          {
            path: 'add', component: AddConsultationComponent,
          },
          {
            path: 'consultation/:id', component: ConsultationComponent,
          },
          {
            path: 'bilan/:id', component: BilanComponent,
          },
          {
            path: 'ordonance/:id', component: OrdonanceComponent,
          }
        ]
      }
    ]
  },
  /*{path:'signIn',
    component:SignInComponent,
  },*/
];
