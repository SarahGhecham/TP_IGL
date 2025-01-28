import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { LaborantinService } from '../../../services/laborantin.service'; // Create this service
import { Chart, registerables } from 'chart.js';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { BilanBiologiqueComponent } from '../../bilan-biologique/bilan-biologique.component';
import { RouterLink, Router } from '@angular/router';
@Component({
  selector: 'app-laborantin',
  imports: [NavbarComponent, ReactiveFormsModule, CommonModule , BilanBiologiqueComponent],
  templateUrl: './laborantin.component.html',
  styleUrls: ['./laborantin.component.scss']
})
export class LaborantinComponent implements OnInit {
  resultatForm: FormGroup;
  courbeForm: FormGroup;
  bilans: any[] = []; // Initialize as an empty array
  graphData: any = null; // For graph data
  chart: any; // For Chart.js instance
  dpiId: any;

  constructor(private fb: FormBuilder, private laborantinService: LaborantinService,private router: Router) {
    this.resultatForm = this.fb.group({
      type_examen: ['', Validators.required],
      resultat: ['', Validators.required],
      date_examen: ['', Validators.required]
    });

    this.courbeForm = this.fb.group({
      dpi_id: ['', Validators.required]
    });

    Chart.register(...registerables); // Register Chart.js
  }

  goToExamen() {
    if (this.courbeForm.get('dpi_id') != null) {
      this.dpiId = this.courbeForm.get('dpi_id')!.value;  // Utilisation de '!'
      console.log(this.dpiId);
      this.router.navigate(['/users/medecin/consultation-dpi/examen-trends', this.dpiId]);
    }
  }

  ngOnInit(): void {
    this.fetchBilanBiologique();
  }

  fetchBilanBiologique() {
    this.laborantinService.getBilanBiologique().subscribe(
      (response: any) => {
        console.log('Bilan biologique:', response[0]);
        // Map the response to the bilans array
        this.bilans = response.map((bilan: any) => ({
         
          id: bilan.id,
          patient_name: bilan.consultation.dpi.patient.username, // Adjust based on your Django model
          status: 'Pending', // Add a default status
          date: bilan.date_bilan
          ,
          comment: bilan.comment
        }));
      },
      (error) => {
        console.error('Error fetching bilan biologique:', error);
      }
    );
  }

  onSubmitResultat() {
    if (this.resultatForm.valid) {
      const resultatData = this.resultatForm.value;
      this.laborantinService.createExamen(resultatData).subscribe(
        (response) => {
          console.log('Resultat saved:', response);
          alert('Resultat saved successfully!');
          this.resultatForm.reset();
        },
        (error) => {
          console.error('Error saving resultat:', error);
          alert('Failed to save resultat.');
        }
      );
    }
  }

  onSubmitCourbe() {
    if (this.courbeForm.valid) {
      const examenType = this.courbeForm.value.examen_type;
      this.laborantinService.generateTrendGraph(examenType).subscribe(
        (response: any) => {
          this.graphData = response;
          this.renderChart();
        },
        (error) => {
          console.error('Error generating trend graph:', error);
          alert('Failed to generate trend graph.');
        }
      );
    }
  }

  renderChart() {
    if (this.chart) {
      this.chart.destroy(); // Destroy existing chart
    }

    const ctx = document.getElementById('trendChart') as HTMLCanvasElement;
    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: this.graphData.dates,
        datasets: [{
          label: this.graphData.examen_type,
          data: this.graphData.resultats,
          borderColor: '#3b82f6',
          fill: false
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `Trend for ${this.graphData.examen_type}`
          }
        }
      }
    });
  }
}