import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConsultationService {

  private baseUrl = 'http://127.0.0.1:8000/api/dpi';

  constructor(private http: HttpClient) {}

  // Obtenir toutes les consultations par NSS
  getAllConsultations(nss: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/${nss}/consultation/all/`);
  }

  // Obtenir une consultation spécifique par ID
  getConsultationById(consultationId: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/consultation/${consultationId}/`);
  }

}
