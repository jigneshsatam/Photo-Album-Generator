import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../_services';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  userName: string = ''; // Assign a default empty string value
  pwd: string = ''; // Assign a default empty string value
  rememberMe: boolean = false; // Assign a default false value
  errorMessage: string = '';

  constructor(private authenticationService: AuthenticationService, private router: Router) { }

  ngOnInit(): void {
  }


  login() {
    this.authenticationService.login(this.userName, this.pwd)
      .subscribe(
        data => {
          console.log(data);
          if (data.role === 'admin') {
            this.router.navigate(['/admin']); // Navigate to admin-landing.component.html
          } else if (data.role === 'guest') {
            this.router.navigate(['/guest']); // Navigate to guest-landing.component.html
          } else {
            this.errorMessage = 'Unexpected user role';
          }
        },
        error => {
          console.log(error);
          if (error.status === 401) {
            this.errorMessage = 'Invalid username or password';
          } else {
            this.errorMessage = 'An unexpected error occurred';
          }
        }
      );
  }

  navigateToAdminRegistration() {
    this.router.navigate(['/register-admin']);
  }

  navigateToGuestRegistration() {
    this.router.navigate(['/register-guest']);
  }



  // login() {
  //   this.authenticationService.login(this.userName, this.pwd)
  //     .subscribe(
  //       data => {
  //         console.log(data);
  //         this.router.navigate(['/']);
  //       },
  //       error => {
  //         console.log('Error:', error); // Add this line to log the error object
  //         if (error.status === 401) {
  //           this.errorMessage = 'Invalid username or password';
  //         } else {
  //           this.errorMessage = 'An unexpected error occurred';
  //         }
  //       }
  //     );
  // }

}
