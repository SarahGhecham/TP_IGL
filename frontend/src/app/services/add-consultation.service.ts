import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AddConsultationService {
  private baseUrl = 'http://localhost:3000/api'; // Remplacez par l'URL de votre backend
  consultationData: any = {}; // Objet pour stocker les données temporairement

  constructor(private http: HttpClient) {} // Obligatoire ici

  // Méthode pour sauvegarder les données
  saveConsultationData(data: any) {
    this.consultationData = data;
  }

  // Méthode pour récupérer les données
  getConsultationData() {
    return this.consultationData;
  }

  PostAddConsultation(endpoint: string, data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/${endpoint}`, data);
  }
}