
import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LaborantinService } from '../../../services/laborantin.service';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

@Component({
  selector: 'app-laborantin',
  imports: [NavbarComponent, ReactiveFormsModule, CommonModule],
  templateUrl: './laborantin.component.html',
  styleUrl: './laborantin.component.scss'
})export class LaborantinComponent implements OnInit {
  createReportForm: FormGroup; // Form group for creating reports
  biologicalReports: any[] = []; // To store the list of reports

  constructor(
    private fb: FormBuilder, // FormBuilder for form initialization
    private laborantinService: LaborantinService
  ) {
    // Initialize the form group
    this.createReportForm = this.fb.group({
      consultationId: ['', [Validators.required]], // Consultation ID field with validation
      reportData: ['', [Validators.required]], // Report Data field with validation
    });
  }

  ngOnInit(): void {
    this.fetchReports(); // Fetch existing reports on initialization
  }

  // Fetch existing reports
  fetchReports(): void {
    this.laborantinService.getbilanBiologiqueList().subscribe(
      (data) => {
        this.biologicalReports = data;
        console.log('this is the biologique data',data);
      },
      (error) => {
        console.error('Error fetching reports:', error);
      }
    );
  }

  // Handle form submission to create a report
  createReport(): void {
    if (this.createReportForm.invalid) {
      alert('Please fill out all required fields.');
      return;
    }

    const formData = this.createReportForm.value; // Extract form data
    this.laborantinService.createBiologicalReport(formData.consultationId, {
      details: formData.reportData,
    }).subscribe(
      (data) => {
        console.log('Report created successfully:', data);
        this.fetchReports(); // Refresh the list
        this.createReportForm.reset(); // Clear the form
      },
      (error) => {
        console.error('Error creating report:', error);
      }
    );
  }
}