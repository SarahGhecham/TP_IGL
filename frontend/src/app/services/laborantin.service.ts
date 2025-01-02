import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LaborantinService {
  private apiUrl = 'http://localhost:8000/api/'; // Adjust the URL based on your Django backend

  constructor(private http: HttpClient) {}

  // Fetch bilan biologique
  getBilanBiologique(): Observable<any> {
    return this.http.get(`${this.apiUrl}bilanBiologique/`);
  }

  // Create examen
  createExamen(examenData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}dpi/consultation/bilanBiologique/1/examen/`, examenData); // Adjust the URL
  }

  // Generate trend graph
  generateTrendGraph(examenType: string): Observable<any> {
    return this.http.get(`${this.apiUrl}dpi/1/${examenType}/`); // Adjust the URL
  }
}