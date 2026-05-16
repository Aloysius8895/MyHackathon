import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { LoginService } from '../login/login-service';

export const authguardGuard: CanActivateFn = (route, state) => {
  const loginService = inject(LoginService);
  const router = inject(Router);

  if (loginService.isLoginValid()) {
    return true;
  } else {
    router.navigate(['/login']);
    return false;
  }
};
