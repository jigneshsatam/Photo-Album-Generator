import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';
import { User } from 'src/app/_models/user';


@Injectable({ 
    providedIn: 'root' 
})
export class UserService {
    constructor(private http: HttpClient, private authService: AuthService) { }

    login(username: string, password: string) {
        return this.http.post<any>('/api/auth/login', { username, password });
    }
}

