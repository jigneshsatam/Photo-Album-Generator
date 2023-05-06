import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { YourService } from '../_services/reset.service'; // Import your service

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent implements OnInit {
  resetPasswordForm: FormGroup;

  constructor(private formBuilder: FormBuilder, private yourService: YourService) {
    this.resetPasswordForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  ngOnInit(): void {}

  submitResetPassword(): void {
    const email = this.resetPasswordForm.get('email')?.value;
    this.yourService.sendResetPasswordEmail(email).subscribe(
      (response) => {
        // Handle successful response, e.g., show success message
      },
      (error) => {
        // Handle error response, e.g., show error message
      }
    );
  }
}
