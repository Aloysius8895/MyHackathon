import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Login } from './login/login';
import { authguardGuard } from './shared/authguard-guard';
import { NotFound } from './shared/not-found/not-found';

export const routes: Routes = [
  {
    path: '',
    component: Home,
    canActivate: [authguardGuard],
  },
  {
    path: 'home',
    component: Home,
    canActivate: [authguardGuard],
  },
  {
    path: 'login',
    component: Login,
  },
  {
    path: '**',
    component: NotFound,
  },
];
