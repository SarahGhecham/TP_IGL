import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LayoutComponent } from './pages/layout/layout.component';
import { MainConsultdpiComponent } from './pages/main-consultdpi/main-consultdpi.component';
import { ConsultationsComponent } from './pages/consultations/consultations.component';
import { AddConsultationComponent } from './pages/add-consultation/add-consultation.component';
import { OrdonanceComponent } from './pages/ordonance/ordonance.component';
import { BilanBiologiqueComponent } from './pages/bilan-biologique/bilan-biologique.component';
import { BilanRadiologiqueComponent } from './pages/bilan-radiologique/bilan-radiologique.component';
//import { SignInComponent } from './pages/sign-in/sign-in.component';
export const routes: Routes = [
  {
    path: '',
    component: LayoutComponent,
    // canActivate: [AuthGuard],
    children: [
      {
        path: 'home', component: HomeComponent,
      },
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
            path: 'bilan-biologique/:id', component: BilanBiologiqueComponent,
          },
          {
            path: 'bilan-radiologique/:id', component: BilanRadiologiqueComponent,
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
