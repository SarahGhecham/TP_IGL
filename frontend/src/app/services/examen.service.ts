import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Examen } from '../models/examen';

@Injectable({
  providedIn: 'root',
})
export class ExamenService {
  private baseUrl = 'http://127.0.0.1:8000/api/dpi/consultation';

  constructor(private http: HttpClient) {}

  getBilanBiologique(consultationId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/${consultationId}/bilanBiologique/`);
  }

  createBilanBiologique(consultationId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/${consultationId}/bilanBiologique/`, {});
  }

  getExamens(consultationId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/bilanBiologique/${consultationId}/examen/`);
  }

  addExamen(consultationId: number, examen: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/bilanBiologique/${consultationId}/examen/`, examen);
  }
}

