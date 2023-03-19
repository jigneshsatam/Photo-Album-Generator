import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-load-images',
  templateUrl: './load-images.component.html',
  styleUrls: ['./load-images.component.css']
})
export class LoadImagesComponent {

  apiUrl = 'http://localhost:8827/';
  imageUrls: string[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.getUrls();
  }

  getUrls() {
    this.http.get<any[]>(this.apiUrl)
      .subscribe((data: any) => {
        console.log("getUrls: ", data)

        console.log("images ngInit: ", this.imageUrls)

        console.log("images ngInit typeof: ", typeof data)
        data["images"].forEach((element: string) => {
          this.imageUrls.push("assets/" + element);
        });

        console.log("images ngInit: ", this.imageUrls)
      },
        error => {
          console.log("getUrls error: ", error);
        });
  }
}
