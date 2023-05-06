import { Component, NgZone } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from './_services';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Photo-Album-Generator';

  constructor(
    private router: Router, 
    private authService: AuthenticationService,
    private ngZone: NgZone // Add NgZone here
  ) {}

  navigateHome() {
    console.log('navigateHome called');
    const userRole = this.authService.userRole.value;
    console.log('User role:', userRole);
  
    const user = this.authService.userValue;
    if (user) {
      this.ngZone.run(() => {
        if (user.role === 'admin') {
          this.router.navigate(['/admin']);
        } else if (user.role === 'guest') {
          this.router.navigate(['/guest']);
        }
      });
    } else {
      this.router.navigate(['/login']);
    }
  }
  

  signOut() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
