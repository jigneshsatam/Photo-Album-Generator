import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import { NgZone } from '@angular/core';

import { environment } from 'src/environments/environment';
import { User } from '../_models';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  private userSubject: BehaviorSubject<User | null>;
  public user: Observable<User | null>;
  public isAdmin$: Observable<boolean>;

  constructor(
    private router: Router,
    private http: HttpClient
  ) {
    this.userSubject = new BehaviorSubject<User | null>(JSON.parse(localStorage.getItem('user')!));
    this.user = this.userSubject.asObservable();
    this.isAdmin$ = this.user.pipe(
      map((user: User | null) => user !== null && user.role === 'admin')
    );
  }

  public get userValue() {
    return this.userSubject.value;
  }

  public userRole: BehaviorSubject<string> = new BehaviorSubject<string>('');

  login(userName: string, pwd: string) {
    return this.http.post<any>(`${environment.apiUrl}/users/login`, { userName, pwd })
      .pipe(
        map(user => {
          // store user details and jwt token in local storage to keep user logged in between page refreshes
          localStorage.setItem('user', JSON.stringify(user));
          this.userSubject.next(user);
          this.userRole.next(user.role); // Set the user role
          return user;
        }),
        catchError(error => {
          // Handle the error and throw it back to the caller
          throw error;
        })
      );
  }

  // login(userName: string, pwd: string) {
  //   return this.http.post<any>(`${environment.apiUrl}/users/login`, { userName, pwd })
  //     .pipe(
  //       map(user => {
  //         // store user details and jwt token in local storage to keep user logged in between page refreshes
  //         localStorage.setItem('user', JSON.stringify(user));
  //         this.userSubject.next(user);
  //         this.userRole.next(user.role); // Set the user role
  //         return user;
  //       }),
  //       catchError(error => {
  //         // Handle the error and throw it back to the caller
  //         throw error;
  //       })
  //     );
  // }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
    this.userSubject.next(null);
    this.router.navigate(['/login']);
  }
}
