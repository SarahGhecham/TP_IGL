//examen-trend.component.ts
import { Component, OnInit,ViewChild} from '@angular/core';
import { ExamenService } from './trend-graph.service'; // Le service qui récupère les données
import { ChartConfiguration, ChartType } from 'chart.js';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { Chart ,registerables} from 'chart.js';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';


Chart.register(...registerables);
//Chart.register(ChartDataLabels);

@Component({
  selector: 'app-examen-trend',
  imports:[NavbarComponent,CommonModule],
  templateUrl: './examen-trend.component.html',
  styleUrls: ['./examen-trend.component.scss']
})
export class ExamenTrendsComponent implements OnInit{
  dpiId: any;
  public NomPatient : String = "Nom";
  charts: { id: string; title: string; unit: string; available: boolean }[] = [
    { id: 'glycemieChart', title: 'Glycemie', unit: 'mg/dl', available: false },
    { id: 'cholesterolChart', title: 'Cholesterol', unit: 'mg/dl', available: false },
    { id: 'hypertensionChart', title: 'Hypertension', unit: 'mmHg', available: false },
  ];
  
  public  config : any = {
    type: 'bar',
    data: {labels: ['A', 'B', 'C'],
      datasets: [{
        label: 'Dataset 1',
        data: [10, 20, 30]
      }]},
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  };
  constructor(private examenService: ExamenService,private route: ActivatedRoute) {}
  @ViewChild('chart') chart: any;
  ngOnInit(): void {
    this.dpiId = this.route.snapshot.paramMap.get('id');
    console.log('ID du DPI:', this.dpiId);
    this.charts.forEach((chart) => {
      this.examenService.getExamenTrends(this.dpiId, chart.title).subscribe((data) => {
        this.NomPatient=data.patient;
        if (data.dates.length > 0 && data.resultats.length > 0) {
          chart.available = true;
          this.loadChart(this.dpiId,chart.title,chart.id);
        }
      });
    });
  }
  
  getBackgroundColor(value: number, examType: string): string {
    // Logique de couleurs basée sur les normes
    if (examType === 'Glycemie') {
      return value >= 70 && value <= 110
        ? 'rgba(61,206,213, 1)' : 'rgba(0, 119, 182, 1)'
    } else if (examType === 'Cholesterol') {
      return value < 200
        ? 'rgba(61,206,213, 1)' : 'rgba(0, 119, 182, 1)'
    } else if (examType === 'Hypertension') {
      return value <= 140 && value>=90
        ? 'rgba(61,206,213, 1)' : 'rgba(0, 119, 182, 1)'
    }
    return 'rgba(128, 128, 128, 0.5)'; // Couleur par défaut
  }
  loadChart(dpiId: string, examType: string, canvasId: string): void {
    this.examenService.getExamenTrends(dpiId, examType).subscribe(
      (data) => {
        // Traitement des données reçues
        this.NomPatient=data.patient;
        const labels = data.dates; // Utilisation des dates comme labels
        const results = data.resultats; // Utilisation des résultats pour l'axe des ordonnées
        
        // Configuration du graphique
        this.config = {
          type: 'bar',
          data: {
            labels: labels, // Dates
            datasets: [{
            data: results, // Les résultats (exemple : [50, 89.1, ...])
            backgroundColor: results.map((value: number) =>
              this.getBackgroundColor(value, examType)
            ),
            borderColor:'rgba(0, 0, 0, 0.1)',
            borderWidth: 3,
            borderRadius: 10, // Coins arrondis
            barPercentage: 0.3, // Largeur des barres
            }],
          },
          options: {
            layout: {
              padding: 15,
            },
            plugins: {
              legend: {
                display: true, // Afficher la légende
                position: 'top', // Position de la légende (haut)
                align: 'end',
                labels: {
                  font: {
                    family: 'Gilroy', // Police locale
                    weight: 'bold',
                    size: 14, // Taille de la police
                  },
                  color: '#333', // Couleur du text
                  generateLabels: () => [
                    {
                      text: 'Dans la Norme',
                      fillStyle: 'rgba(61,206,213, 1)',
                      hidden: false,
                    },
                    {
                      text: 'Hors Norme',
                      fillStyle: 'rgba(0, 119, 182, 1)',
                      hidden: false,
                    },
                  ],
                  //usePointStyle: true, // Utilisation des carrés
                  boxWidth: 15,
                  boxHeight: 15
                },
            },
          },
            scales: {
              x: {
                border: {
                  width: 3,
                },
                grid: {
                  display: false,
                },
                ticks: {
                  font: {
                    family: 'Gilroy', // Police locale
                    size: 14, // Taille de la police
                  },
                },
                
              },
              y: {
                border: {
                  width: 3,
                },
                grid: {
                  color: 'rgba(0, 119, 182, 0.10)',
                },
                ticks: {
                  font: {
                    family: 'Gilroy', // Police locale
                    size: 14, // Taille de la police
                  },
                },
                beginAtZero: true
              }
            }
          }
        };
        
        this.chart = new Chart(canvasId, this.config);
              
      },
    );
  }
  }


