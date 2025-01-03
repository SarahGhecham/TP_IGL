import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AddConsultationService {
  private baseUrl = 'http://localhost:8000/dpi/consultation/'; // Modifiez selon votre backend

  constructor(private http: HttpClient) {}

  createConsultation(consultation: { date: string; motif: string }): Observable<any> {
    return this.http.post(this.baseUrl, consultation);
  }
}