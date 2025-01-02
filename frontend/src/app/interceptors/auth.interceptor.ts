import { HttpInterceptorFn } from '@angular/common/http';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access');

  // Define routes to skip
  const excludedRoutes = ['/api/login'];

  // Check if the current request URL includes any excluded route
  if (excludedRoutes.some((route) => req.url.includes(route))) {
    return next(req); // Skip adding the Authorization header
  }

  // Attach token to other requests
  if (token) {
    const cloned = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
    return next(cloned);
  }

  return next(req); // Proceed without adding token if no token exists
};
