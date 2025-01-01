import { Component } from '@angular/core';
import { NavbarComponent } from '../../../shared/navbar/navbar.component';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-infirmier',
  standalone: true,
  imports: [NavbarComponent, ReactiveFormsModule, CommonModule],
  templateUrl: './infirmier.component.html',
  styleUrl: './infirmier.component.scss'
})
export class InfirmierComponent {
  soinForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.soinForm = this.fb.group({
      dpi: ['', Validators.required],
      description: ['', Validators.required],
      date_soin: ['', Validators.required],
      observations: ['']
    });
  }

  onSubmit() {
    if (this.soinForm.valid) {
      console.log(this.soinForm.value);
      // Here you'll add your service call
    }
  }
}