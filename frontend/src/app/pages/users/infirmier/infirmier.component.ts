import { Component, OnInit } from '@angular/core';
import { SoinService } from '../../../services/soin.service';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';

@Component({
  selector: 'app-infirmier',
  imports: [NavbarComponent, ReactiveFormsModule, CommonModule],
  templateUrl: './infirmier.component.html',
  styleUrls: ['./infirmier.component.scss']
})
export class InfirmierComponent implements OnInit {
  careForm: FormGroup;
  patients: any[] = []; // Initialize as an empty array
  selectedPatient: any = null; // Initialize as null

  constructor(private fb: FormBuilder, private soinService: SoinService) {
    this.careForm = this.fb.group({
      dpi: ['', Validators.required],
      description: ['', Validators.required],
      date_soin: ['', Validators.required],
      observations: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.fetchDPIList();
  }

  fetchDPIList() {
    this.soinService.getDPIList().subscribe(
      (response: any) => {
        // Map the response to the patients array
        this.patients = response.map((dpi: any) => ({
          id: dpi.id,
          name: dpi.patient.user.get_full_name, // Adjust based on your Django model
          nss: dpi.nss,
          status: 'Active', // Add a default status
          room: '101', // Add a default room
          gender: 'Male', // Add a default gender
          age: this.calculateAge(dpi.date_naissance), // Calculate age from date of birth
          address: dpi.adresse,
          phone: dpi.telephone,
          email: 'tipaza.com', // Add a default email
          emergencyContact: dpi.personne_a_contacter
        }));
        // Set the first patient as selected
        if (this.patients.length > 0) {
          this.selectedPatient = this.patients[0];
        }
      },
      (error) => {
        console.error('Error fetching DPI list:', error);
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

  selectPatient(patient: any) {
    this.selectedPatient = patient;
  }

  onSubmit() {
    if (this.careForm.valid) {
      const careData = this.careForm.value;
      this.soinService.createSoin(careData).subscribe(
        (response) => {
          console.log('Care entry saved:', response);
          alert('Care entry saved successfully!');
          this.careForm.reset();
        },
        (error) => {
          console.error('Error saving care entry:', error);
          alert('Failed to save care entry.');
        }
      );
    }
  }
}