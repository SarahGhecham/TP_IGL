import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class OrdonnanceService {
  private apiUrl = 'http://localhost:8000/api/dpi/consultation/ordonnance/create/';

  constructor(private http: HttpClient) {}

  createOrdonnance(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }
}
