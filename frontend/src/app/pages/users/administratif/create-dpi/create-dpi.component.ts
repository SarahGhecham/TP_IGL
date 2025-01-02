  import { Component, OnInit } from '@angular/core';
  import { FormBuilder, FormGroup, Validators } from '@angular/forms';
  import { NavbarComponent } from '../../../../shared/navbar/navbar.component';
  import { Router, RouterModule } from '@angular/router';
  import { CommonModule } from '@angular/common';
  import { ReactiveFormsModule } from '@angular/forms';
  import { DpiService } from '../../../../services/dpi.service';
  import { HttpErrorResponse } from '@angular/common/http';

  @Component({
    selector: 'app-create-dpi',
    templateUrl: './create-dpi.component.html',
    styleUrls: ['./create-dpi.component.scss'],
    imports: [NavbarComponent, CommonModule, ReactiveFormsModule, RouterModule]
  })
  export class CreateDPIComponent implements OnInit {

    dpiForm!: FormGroup;
    isLoading = false; 
    errorMessage = ''; 
    successMessage = ''; 
    
    constructor(private fb: FormBuilder, private router: Router, private dpiService: DpiService) {}

    ngOnInit() {
      this.dpiForm = this.fb.group({
        patient: ['', Validators.required],
        medecin_traitant: ['', Validators.required],
        nss: ['', [Validators.required, Validators.pattern(/^\d{15}$/)]],
        date_naissance: ['', Validators.required],
        adresse: ['', Validators.required],
        telephone: ['', [Validators.required, Validators.pattern(/^[0-9]{10}$/)]],
        mutuelle: [''],
        personne_a_contacter: ['', Validators.required]
      });
    }

    onBack() {
      // Redirect to the previous page
      this.router.navigate(['/users/administratif']); 

    }
    onSubmit() {
      if (this.dpiForm.valid) {
        this.isLoading = true;
        this.errorMessage = '';
        const dpiData = this.dpiForm.value;
  
        this.dpiService.createDPI(dpiData).subscribe({
          next: (response) => {
            console.log('DPI Created:', response);
            this.isLoading = false;
            this.successMessage = 'DPI ajouté avec succès';


            setTimeout(() => {
            this.successMessage = ''; 
            this.router.navigate(['/users/administratif']); // Redirect on success
          }, 3000);
          },
          error: (error: HttpErrorResponse) => {
            this.isLoading = false;
            this.errorMessage = error.error?.detail || 'An error occurred while creating the DPI.';
            console.error('Error:', error);
          }
        });
      } else {
        this.markFormGroupTouched(this.dpiForm);
      }
    }
    markFormGroupTouched(formGroup: FormGroup) {
      Object.values(formGroup.controls).forEach(control => {
        control.markAsTouched();

        if (control instanceof FormGroup) {
          this.markFormGroupTouched(control);
        }
      });
    }
  }