import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BilanRadiologiqueService {
  private apiUrl = '/api/bilans'; // Base URL pour les endpoints des bilans

  constructor(private http: HttpClient) {}

  getBilanByNss(nss: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/${nss}`);
  }

  addBilan(bilan: { nom: string; date: string }): Observable<any> {
    return this.http.post(this.apiUrl, bilan);
  }
}
