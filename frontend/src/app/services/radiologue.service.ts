import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RadiologueService {
  private apiUrl = 'http://localhost:8000/api/';
  private apiUrl2 = 'http://localhost:8000/dpi/';

  constructor(private http: HttpClient) {}

  // Fetch bilan radiologique
  getBilanRadiologique(): Observable<any> {
    return this.http.get(`${this.apiUrl2}bilanRadiologique`);
  }

  // Create compte rendu
  createCompteRendu(resultatExamenId: number, compteRenduData: any): Observable<any> {
    return this.http.post(`${this.apiUrl2}resultats/${resultatExamenId}/compte-rendu/create/`, compteRenduData);
  }

  // Upload radio image
  uploadRadioImage(resultatExamenId: number, formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl2}resultats/create/`, formData);
  }
}