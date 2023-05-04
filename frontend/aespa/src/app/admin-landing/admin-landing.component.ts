import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-landing',
  templateUrl: './admin-landing.component.html',
  styleUrls: ['./admin-landing.component.css']
})

export class AdminLandingComponent {

  apiUrl = 'http://localhost:8827/images/albums';
  albums: any[] = [];
  selectedAlbum: any = {};
  isLoading: boolean = false;

  constructor(private http: HttpClient, private router: Router) { }

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

  onDelete(album: any) {
    this.selectedAlbum = album;
  }

  deleteAlbum(id: number) {
    this.http.delete<any>(this.apiUrl + "/" + this.selectedAlbum.id)
      .subscribe((data: any) => {
        this.getAlbums();
      },
        error => {
          console.log("deleteAlbum error: ", error);
        });
  }

  onNewDirectory() {
    this.router.navigate(['../admin/upload']);
  }

  onAddGuest() {
    this.router.navigate(['../register-guest']);
  }

  onSlideshow() {
    this.router.navigate(['../guest/load-images']);
  }

  onLoadImages(album: any) {
    const id = album.id;
    this.router.navigate([`/admin/${id}/load-images`]);
  }

}
