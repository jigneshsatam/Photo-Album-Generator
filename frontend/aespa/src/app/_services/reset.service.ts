import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class YourService {
  constructor(private http: HttpClient) {}

  sendResetPasswordEmail(email: string): Observable<any> {
    const apiUrl = 'https://your-api-url/reset-password';
    return this.http.post(apiUrl, { email: email });
  }
}
