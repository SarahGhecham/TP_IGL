import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card'
import { NavbarComponent } from '../../../../shared/navbar/navbar.component';
import { MatIconModule } from '@angular/material/icon';
import { CalendarComponent } from '../../../../shared/calendar/calendar.component';
import { HttpClient ,HttpErrorResponse} from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-home',
  imports: [MatCardModule,NavbarComponent,MatIconModule,CalendarComponent,CommonModule,FormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeMedComponent implements OnInit{

  patients: any[] = []; // Liste de patients pour l'affichage initial
  searchedPatient: any = null;

  nss: string = ''; // Variable pour stocker la valeur du champ de recherche
  patient: any; // Variable pour stocker les résultats du patient
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadPatients();  // Charger plusieurs patients initialement
  }

  loadPatients() {
    this.http.get<any[]>(`${this.apiUrl}/patients`)  // Remplacez avec l'URL de votre API
      .subscribe({
        next: (data) => {
          this.patients = data.slice(0, 3);  // Afficher les 3 premiers patients
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des patients:', err);
        }
      });
  }

  searchPatient() {
    if (this.nss) {

      this.http.get(`${this.apiUrl}/search-dpi-by-nss/${this.nss}/`,/*{headers}*/).subscribe(
        (response) => {
          if (!response) { // Si la réponse indique une erreur ou un 404
            this.patient = null; // Réinitialise l'objet patient
            console.log("Patient non trouvé, chargement des patients initiaux.");
            this.loadPatients(); 
          }else{
          this.patient = response; // Stocke les résultats de la recherche
          this.patients = [];
          console.log(this.patient); }// Affiche les résultats dans la console pour le débogage
        },
        (error) => {
          console.error('Erreur lors de la recherche du patient:', error);
          this.patient = null; // Réinitialise l'objet patient
            console.log("Patient non trouvé, chargement des patients initiaux.");
            this.loadPatients(); 
        }
      );
    }else{
      console.log("Pas de nss");
    }
  }
  resetSearch() {
    this.patient= null;
    this.loadPatients();  // Recharger la liste initiale de patients
  }

  triggerFileInput(): void {
    const fileInput = document.querySelector<HTMLInputElement>('#fileInput');
    if (fileInput) {
      fileInput.click();
    }
  }

  // Gestion de la sélection de fichier
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
  

    if (input?.files?.length) {
      const file = input.files[0];
      console.log('Fichier sélectionné:', file);

      // Appeler la méthode pour envoyer le fichier
      input.value = '';
      this.uploadFile(file);
    }
  }

  // Envoi du fichier au backend
  uploadFile(file: File): void {
    const formData = new FormData();
    formData.append('file', file);
    console.log("Données envoyées : ", formData);
    
    this.http.post('http://127.0.0.1:8000/api/search-dpi-by-qr/', formData).subscribe(
      (response) => {
        if (!response) { // Si la réponse indique une erreur ou un 404
          this.patient = null; // Réinitialise l'objet patient
          console.log("Patient non trouvé, chargement des patients initiaux.");
          this.loadPatients(); 
        }else{
        this.patient = response; // Stocke les résultats de la recherche
        this.patients = [];
        console.log(this.patient); }// Affiche les résultats dans la console pour le débogage
      },
      (error) => {
        console.error('Erreur lors de la recherche du patient:', error);
        this.patient = null; // Réinitialise l'objet patient
          console.log("Patient non trouvé, chargement des patients initiaux.");
          this.loadPatients(); 
      }
    );


}
}
