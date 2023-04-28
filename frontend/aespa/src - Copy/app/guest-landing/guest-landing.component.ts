import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-guest-landing',
  templateUrl: './guest-landing.component.html',
  styleUrls: ['./guest-landing.component.css']
})
export class GuestLandingComponent {
  apiUrl = 'http://localhost:8827/images/albums';
  albums: any[] = [];
  selectedAlbum: any = {};
  isLoading: boolean = false;

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getAlbums();
  }

  getAlbums() {
    this.isLoading = true;
    this.http.get<any>(this.apiUrl)
      .subscribe((data: any) => {
        this.albums = data["albums"];
        this.isLoading = false;
      },
        error => {
          console.log("getAlbums error: ", error);
        });
  }
}
