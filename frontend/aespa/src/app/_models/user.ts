import { Role } from "./role";

export interface User {
    id: number;
    username: string;
    password: string;
    firstName: string;
    lastName: string;
    role: 'admin' | 'guest'; // Add this line to define the role property type
    token?: string;
  }
  