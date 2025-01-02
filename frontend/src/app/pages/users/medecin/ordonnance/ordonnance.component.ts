import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../../../../shared/navbar/navbar.component';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { OrdonnanceService } from '../../../../services/ordonnance.service'; 

@Component({
  selector: 'app-ordonnance',
  imports: [NavbarComponent, CommonModule, ReactiveFormsModule],
  templateUrl: './ordonnance.component.html',
  styleUrls: ['./ordonnance.component.scss'],
})
export class OrdonnanceComponent {
  ordonnanceForm: FormGroup;
  successMessage: string = '';
  errorMessage: string = '';
  patientName = 'sawaniMrid';
  readonly consultationId = 2; 

  constructor(private fb: FormBuilder, private ordonnanceService: OrdonnanceService) {
    this.ordonnanceForm = this.fb.group({
      date_ordonnance: ['', Validators.required],
      text: ['', [Validators.required, Validators.minLength(10)]],
    });
  }

  onSubmit() {
    if (this.ordonnanceForm.valid) {
      // Add consultation ID to the request payload
      const payload = {
        ...this.ordonnanceForm.value,
        consultation: this.consultationId,
      };

      this.ordonnanceService.createOrdonnance(payload).subscribe({
        next: (response) => {
          console.log('Ordonnance created:', response);
          this.successMessage = 'Ordonnance soumise avec succès!';
          this.errorMessage = '';
          this.ordonnanceForm.reset();
        },
        error: (err) => {
          console.error('Error:', err);
          this.successMessage = '';
          this.errorMessage = 'Une erreur s’est produite lors de la soumission.';
        },
      });
    } else {
      this.successMessage = '';
      this.errorMessage = 'Veuillez remplir tous les champs correctement.';
    }
  }

  onBack() {
    window.history.back();
  }
}
