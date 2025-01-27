import { Component, OnInit } from '@angular/core';
import { RouterLink, Router } from '@angular/router';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-main-consultdpi',
  imports: [NavbarComponent,CommonModule],
  templateUrl: './main-consultdpi.component.html',
  styleUrl: './main-consultdpi.component.scss'
})
export class MainConsultdpiComponent implements OnInit{
  dpiId: any;
  dpiData: any = null;
  patientData: any = null;

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.dpiId = this.route.snapshot.paramMap.get('id');
    console.log('ID du DPI:', this.dpiId);
    if (this.dpiId) {
      this.getDPI(this.dpiId);
    }
  }

  getDPI(id: number): void {
    const apiUrl = `http://127.0.0.1:8000/api/dpi/${id}`;
    this.http.get(apiUrl).subscribe({
      next: (data) => {
        this.dpiData = data;
        console.log('DPI Data:', this.dpiData);
      },
      error: (err) => {
        console.error('Erreur lors de la récupération du DPI:', err);
      },
    });
    this.http.get(`http://127.0.0.1:8000/api/dpi/get-dpi/${this.dpiData.nss}/`).subscribe({
        next: (data) => {
          this.patientData = data;
          console.log('DPI Data:', data);
        },
        error: (err) => {
          console.error('Erreur lors de la récupération du DPI:', err);
        },
    });
  }

  navigateTo(page: string): void {
    if (this.dpiData) {
      const nss = this.dpiData.nss;
      this.router.navigate([`/${page}`], {
        queryParams: { id: this.dpiId, nss: nss },
      });
    }
  }
}
