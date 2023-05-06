import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from 'src/environments/environment';
import { User } from '../_models';

@Injectable({ providedIn: 'root' })
export class UserService {
    login(username: any, password: any) {
        throw new Error('Method not implemented.');
    }
    createList(arg0: string) {
        throw new Error('Method not implemented.');
    }
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/users`);
    }

    getById(id: number) {
        return this.http.get<User>(`${environment.apiUrl}/users/${id}`);
    }
}