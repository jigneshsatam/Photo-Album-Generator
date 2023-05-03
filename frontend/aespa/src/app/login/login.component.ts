import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../_services';
import { of } from 'rxjs';
import { AuthenticationService } from '../_services';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
    username: string = '';
    password: string = '';
    rememberMe: boolean = false; // Add this line
    errorMessage: string = '';

  constructor(private authenticationService: AuthenticationService, private router: Router) { }

  ngOnInit(): void {
  }

  login() {
    this.authenticationService.login(this.username, this.password)
      .subscribe(
        data => {
          console.log(data);
          this.router.navigate(['/']);
        },
        error => {
          console.log(error);
          this.errorMessage = 'Invalid username or password';
        }
      );
  }

}

//   login() {
//     this.userService.login(this.username, this.password)
//       .subscribe(
//         data => {
//           console.log(data);
//           this.router.navigate(['/']);
//         },
//         error => {
//           console.log(error);
//           this.errorMessage = 'Invalid username or password';
//         }
//       );
//   }
// }

  
  
//   login() {
//     this.userService.login(this.username, this.password)
//         .subscribe(
//             data => {
//                 this.router.navigate(['/']);
//             },
//             error => {
//                 console.log(error);
//                 this.errorMessage = 'Invalid username or password';
//             });
//         }



//   createNewList() {
//     of(this.userService.createList("testing list"))
//     .subscribe((res: any) => {
//       console.log(res)
//     })
//   }



// }
