import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Image } from "./image";

@Component({
  selector: 'app-load-images',
  templateUrl: './load-images.component.html',
  styleUrls: ['./load-images.component.css']
})
export class LoadImagesComponent {

  apiUrl = 'http://localhost:8827/images/load';
  images: Image[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getImages();
  }

  getImages() {
    this.http.get<any>(this.apiUrl)
      .subscribe((data: any) => {
        data["images"].forEach((element: Image) => {
          element["path"] = "assets/" + element.path;
          this.images.push(element);
        });

      },
        error => {
          console.log("getImages error: ", error);
        });
  }
}
