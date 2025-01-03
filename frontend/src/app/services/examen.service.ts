import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Examen } from '../models/examen';

@Injectable({
  providedIn: 'root',
})
export class ExamenService {
  private readonly apiUrl = 'http://votre-api-url/examens'; // URL de l'API

  constructor(private http: HttpClient) {}

  // Méthode pour récupérer les bilans biologiques
  getBilanBiologique(): Observable<Date> {
    return this.http.get<{ date: string }>(`${this.apiUrl}/bilan-biologique`).pipe(
      map((data) => new Date(data.date)) // Convertir la chaîne de caractères en `Date`
    );
  }

  // Endpoint pour ajouter un examen
  addExamen(examen: Examen): Observable<Examen> {
    return this.http.post<Examen>(`${this.apiUrl}/add`, examen);
  }

  // Endpoint pour récupérer tous les examens
  getExamens(): Observable<Examen[]> {
    return this.http.get<Examen[]>(this.apiUrl); // Appel GET pour récupérer les examens
  }
}

