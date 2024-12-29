import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const AuthGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isLoggedIn()) {
    console.log('User not logged in, redirecting to login page');
    router.navigate(['/login']);
    return false;
  }

  const userRole = authService.getRole(); 
  const routeRole = route.routeConfig?.path?.split('/')[1]; 
  console.log(userRole);
  if (userRole === routeRole) {
    return true; // Role matches, allow access
  } else {
    console.log(`Role mismatch! Redirecting to /users/${userRole}`);
    router.navigate([`/users/${userRole}`]);
    return false;
  }
};
