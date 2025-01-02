import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SoinService {
  private apiUrl = 'http://localhost:8000/dpi/soin/create/'; // Replace with your API URL
  private apiUrl2= 'http://localhost:8000/api/dpi/'; // Replace with your API URL
  constructor(private http: HttpClient) {}
  
  createSoin(soinData: any): Observable<any> {
    return this.http.post(this.apiUrl, soinData);
  }
  getDPIList(): Observable<any> {
    return this.http.get(this.apiUrl2);
  }
}