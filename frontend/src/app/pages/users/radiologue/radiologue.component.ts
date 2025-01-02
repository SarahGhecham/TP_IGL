import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RadiologueService } from '../../../services/radiologue.service'; // Create this service
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-radiologue',
  imports: [NavbarComponent, ReactiveFormsModule, CommonModule],
  templateUrl: './radiologue.component.html',
  styleUrls: ['./radiologue.component.scss']
})
export class RadiologueComponent implements OnInit {
  compteRenduForm: FormGroup;
  radioImageForm: FormGroup;
  bilans: any[] = []; // Initialize as an empty array
  selectedBilan: any = null; // Initialize as null
  selectedFile: File | null = null; // For file upload

  constructor(private fb: FormBuilder, private radiologueService: RadiologueService) {
    this.compteRenduForm = this.fb.group({
      compte_rendu: ['', Validators.required]
    });

    this.radioImageForm = this.fb.group({
      radio_image: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.fetchBilanRadiologique();
  }
  onBilanSelect(bilan: any): void {
    this.selectedBilan = bilan;
  }
  fetchBilanRadiologique() {
    this.radiologueService.getBilanRadiologique().subscribe(
    
      (response: any) => {
        console.log('Bilan radiologique:', response[0])
        // Map the response to the bilans array
        this.bilans = response.map((bilan: any) => ({
          id: bilan.id,
          patient_name: bilan.consultation.dpi.patient.username, // Adjust based on your Django model
          nss: bilan.consultation.dpi.nss,
          status: 'Pending', // Add a default status
          date: bilan.date,
          type: bilan.consultation.motif,
          gender: 'Male', // Add a default gender
          age: this.calculateAge(bilan.consultation.dpi.date_naissance), // Calculate age from date of birth
          address: bilan.consultation.dpi.patient.adresse,
          phone: bilan.consultation.dpi.telephone,
          email: bilan.consultation.dpi.email, // Add a default email
          emergencyContact: bilan.consultation.dpi.personne_a_contacter,
          image:bilan.image
        }));
        // Set the first bilan as selected
        if (this.bilans.length > 0) {
          this.selectedBilan = this.bilans[0];
        }
      },
      (error) => {
        console.error('Error fetching bilan radiologique:', error);
      }
    );
  }

  calculateAge(dateOfBirth: string): number {
    const dob = new Date(dateOfBirth);
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
      age--;
    }
    return age;
  }

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
    }
  }

  onSubmitCompteRendu() {
    if (this.compteRenduForm.valid) {
      const compteRenduData = this.compteRenduForm.value;
      this.radiologueService.createCompteRendu(this.selectedBilan.id, compteRenduData).subscribe(
        (response) => {
          console.log('Compte rendu saved:', response);
          alert('Compte rendu saved successfully!');
          this.compteRenduForm.reset();
        },
        (error) => {
          console.error('Error saving compte rendu:', error);
          alert('Failed to save compte rendu.');
        }
      );
    }
  }

  onSubmitRadioImage() {
    if (this.radioImageForm.valid && this.selectedFile) {
      const formData = new FormData();
      formData.append('radio_image', this.selectedFile);

      this.radiologueService.uploadRadioImage(this.selectedBilan.id, formData).subscribe(
        (response) => {
          console.log('Radio image uploaded:', response);
          alert('Radio image uploaded successfully!');
          this.radioImageForm.reset();
        },
        (error) => {
          console.error('Error uploading radio image:', error);
          alert('Failed to upload radio image.');
        }
      );
    }
  }
}