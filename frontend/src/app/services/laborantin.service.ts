import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LaborantinService {
  private apiUrl = 'http://127.0.0.1:8000/api'; // Replace with your backend URL

  constructor(private http: HttpClient) {}

  // Fetch all biological reports
  getbilanBiologiqueList(): Observable<any> {
    return this.http.get(`${this.apiUrl}/bilanBiologique/`);
  }

  // Fetch a specific biological report by consultation ID
  getBiologicalReportByConsultationId(consultationId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/bilan-biologique/${consultationId}/`);
  }

  // Create a new biological report
  createBiologicalReport(consultationId: number, data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/bilan-biologique/${consultationId}/`, data);
  }

  // Update an existing biological report
  updateBiologicalReport(consultationId: number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/bilan-biologique/${consultationId}/`, data);
  }

  // Delete a biological report
  deleteBiologicalReport(consultationId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/bilan-biologique/${consultationId}/`);
  }
}
