import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../login/login-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {
  constructor(private loginService: LoginService) {}
  showNavLinks = false;
  imageUrl = '';

  ngOnInit(): void {
    this.loginService.loginNotification.subscribe((message) => {
      this.showNavLinks = message;
      if (message) {
        this.imageUrl = this.loginService.getLoginImage();
      }
    });
  }

  logOutUser() {
    this.loginService.signOut();
  }
}
