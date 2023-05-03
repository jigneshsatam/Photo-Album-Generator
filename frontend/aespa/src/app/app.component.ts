import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from './_services/authentication.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  constructor(
    private router: Router,
    private authenticationService: AuthenticationService
  ) { }
  title = 'aespa';

  logout() {
    this.authenticationService.logout();
    this.router.navigate(['/login']);
  }

  isLoggedIn() {
    return this.authenticationService.currentUserValue;
  }
  
}
