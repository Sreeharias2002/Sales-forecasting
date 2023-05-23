import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private router: Router, private http: HttpClient) { }

  isAuthenticated(): boolean {
    if (sessionStorage.getItem('token') !== null) {
      return true;
    }
    return false;
  }

  canAccess() {
    if (!this.isAuthenticated()) {
      this.router.navigate(['/login']);
    }
  }
  canAuthenticated(){
    if (this.isAuthenticated()) {
      this.router.navigate(['/']);
    }
  }

  register(name: string, email: string, password: string) {
    return this.http.post<{ idToken: string }>("https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyA0dE99PEJlb0N-KoEv-naA_x61NB6ewTE",
      {
        displayName: name,
        email: email,
        password: password
      })
  }

  storeToken(token: string) {
    sessionStorage.setItem('token', token);
  }

  login(email:string, password:string){
    return this.http.post<{idToken:string}>("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyA0dE99PEJlb0N-KoEv-naA_x61NB6ewTE",
    {
      email,password
    })
  }

  removeToken(){
    sessionStorage.removeItem("token");
  }
  
}
