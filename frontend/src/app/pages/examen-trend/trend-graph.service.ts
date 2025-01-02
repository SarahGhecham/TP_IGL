//trend-graph.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpClientModule } from '@angular/common/http';
import { response } from 'express';

@Injectable({
  providedIn: 'root'
})
export class ExamenService {
  private apiUrl = 'http://127.0.0.1:8000/api/dpi'; 

  constructor(private http: HttpClient) {}

  getExamenTrends(dpiId: string, examenType: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${dpiId}/${examenType}`).pipe(
      catchError((error: any) => {
        console.warn(`Erreur lors de la récupération des données pour ${examenType}:`, error.message,error.error.patient);
        // Retourne un Observable contenant un objet vide ou des données par défaut
        return of({
          patient: error.error.patient,
          dates: [],
          resultats: [],
        });
      })
    );
  }
  
}


