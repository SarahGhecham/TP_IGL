import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { catchError, throwError, tap } from 'rxjs';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient, private router: Router) {
    console.log('AuthService instantiated');
  }

  /**
   * Login the user and store tokens on success.
   */
  login(username: string, password: string) {
    return this.http.post(`${this.apiUrl}/login/`, { username, password }).pipe(
      tap((response: any) => {
        this.storeTokens(response.access, response.refresh);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Logout the user and clear tokens.
   */
  logout() {
    const refreshToken = localStorage.getItem('refresh');
    if (!refreshToken) {
      this.clearTokens();
      this.router.navigate(['/login']);
      return;
    }

    this.http.post(`${this.apiUrl}/logout/`, { refresh: refreshToken }).pipe(
      tap(() => this.clearTokens()),
      catchError(() => {
        this.clearTokens(); // Clear tokens even if logout fails
        return throwError(() => new Error('Logout failed.'));
      })
    ).subscribe(() => this.router.navigate(['/login']));
  }

  /**
   * Refresh the access token.
   */
  refreshToken() {
    const refreshToken = localStorage.getItem('refresh');
    if (!refreshToken) {
      this.logout(); // Logout if refresh token is missing
      return;
    }

    return this.http.post(`${this.apiUrl}/token/refresh/`, { refresh: refreshToken }).pipe(
      tap((response: any) => {
        this.storeTokens(response.access, response.refresh); // Update tokens
        localStorage.setItem('role', response.role);
      }),
      catchError(() => {
        this.logout(); // Logout if refreshing the token fails
        return throwError(() => new Error('Session expired. Please log in again.'));
      })
    );
  }

  /**
   * Utility to store tokens.
   */
  storeTokens(access: string, refresh: string) {
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
  }

  /**
   * Get the access token.
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access');
  }

  /**
   * Decode JWT and extract payload.
   */
  private decodeToken(token: string): any {
    try {
      return jwtDecode(token);
    } catch (error) {
      console.error('Invalid token:', error);
      return null;
    }
  }

  /**
   * Get the payload of the access token.
   */
  getTokenPayload(): any {
    const token = this.getAccessToken();
    if (!token) {
      console.error('No access token found.');
      return null;
    }

    const decoded = this.decodeToken(token);
    console.log('Decoded Payload:', decoded); // Log for debugging
    return decoded;
  }

  /**
   * Get the username from the access token.
   */
  getUsername(): string | null {
    const payload = this.getTokenPayload();
    return payload ? payload.username : null; // Adjust the key based on your JWT structure
  }

  /**
   * Clear tokens from localStorage.
   */
  clearTokens() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('role');
  }

  /**
   * Check if the user is logged in.
   */
  isLoggedIn(): boolean {
    return !!this.getAccessToken();
  }

  /**
   * Handle errors from HTTP requests.
   */
  private handleError(error: HttpErrorResponse) {
    if (error.status === 401) {
      this.logout(); // Automatically logout on unauthorized errors
    }
    return throwError(() => new Error(error.message || 'Server error.'));
  }
}
