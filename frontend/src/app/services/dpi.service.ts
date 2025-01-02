import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DpiService {
  private apiUrl = 'http://localhost:8000/api/dpi/create/'; // API Endpoint

  constructor(private http: HttpClient) {}

  /**
   * Create a new DPI.
   * @param dpiData The data for the new DPI.
   * @returns Observable with the created DPI or error.
   */
  createDPI(dpiData: any): Observable<any> {
    return this.http.post(this.apiUrl, dpiData);
  }
}
