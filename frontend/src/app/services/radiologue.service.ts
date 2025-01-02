import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RadiologueService {
  private apiUrl = 'http://localhost:8000/api/'; // Adjust the URL based on your Django backend

  constructor(private http: HttpClient) {}

  // Fetch bilan radiologique
  getBilanRadiologique(): Observable<any> {
    return this.http.get(`${this.apiUrl}bilanRadiologique/`);
  }

  // Create compte rendu
  createCompteRendu(resultatExamenId: number, compteRenduData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}resultats/${resultatExamenId}/compte-rendu/create/`, compteRenduData);
  }

  // Upload radio image
  uploadRadioImage(resultatExamenId: number, formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}resultats/create/`, formData);
  }
}