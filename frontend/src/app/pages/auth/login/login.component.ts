import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loginForm: FormGroup;
  hidePassword = true;
  errorMessage: string | null = null; // To display error messages

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]], // Ensure alignment with backend
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  togglePasswordVisibility() {
    this.hidePassword = !this.hidePassword;
  }

  onSubmit() {
    if (this.loginForm.invalid) {
      this.errorMessage = '⚠️ Please fill in the form correctly!';
      return;
    }
  
    const { username, password } = this.loginForm.value;
  
    this.authService.login(username, password).subscribe({
      next: (response: any) => {
        console.log('✅ Login successful. Tokens stored successfully.');
        this.errorMessage = null; // Clear error message
        
        const role = response.role || localStorage.getItem('role');
        localStorage.setItem('role', role);
        console.log('Role:', role);
        if (role) {
          this.router.navigate([`/users/${role}`]); // Redirect based on role
        } else {
          this.router.navigate(['/']); // Fallback redirect
        }

      },
      error: (error) => {
        console.error('Login error:', error);
        
        // Display specific error messages based on status code
        switch (error.status) {
          case 401:
            this.errorMessage = '❌ Invalid username or password. Please try again.';
            break;
          case 404:
            this.errorMessage = '❌ Invalid username or password. Please try again.';
            break;
          case 400:
            this.errorMessage = '❌ Bad request. Please check your input.';
            break;
          case 0:
            this.errorMessage = '❌ Network error. Please check your connection.';
            break;
          default:
            this.errorMessage = '❌ An unexpected error occurred. Please try again later.';
        }
      },
    });
  }
  

  onBack() {
    this.router.navigate(['/']); // Navigate back to a landing or previous page
  }
}
