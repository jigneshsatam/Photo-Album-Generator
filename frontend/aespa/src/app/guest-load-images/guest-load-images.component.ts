import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Image } from "./image";
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-load-images',
  templateUrl: './guest-load-images.component.html',
  styleUrls: ['./guest-load-images.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class GuestLoadImagesComponent {
  heroForm: any;
  tags: any[] = [
  ];
  apiUrl = 'http://localhost:8827/images/load?directory=uploads/images';
  getTagUrl = 'http://localhost:8827/tags/fetchTags';
  images: Image[] = [];

  constructor(private http: HttpClient, private fb: FormBuilder) { }

  ngOnInit() {
    this.getImages();
    this.getTags();
    this.heroForm = this.fb.group({
      selectedTagIds: [],
    });
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

  getTags() {
    this.http.get<any>(this.getTagUrl)
      .subscribe((data: any) => {
        this.tags = data.tags;
      },
        error => {
          console.log("getImages error: ", error);
        });
  }

  selectAll() {
    this.heroForm.get('selectedTagIds').setValue(this.tags);
  }

  unselectAll() {
    this.heroForm.get('selectedTagIds').setValue([]);
  }

  addCustomTag = (term: string) => {
    this.tags = this.tags.concat({ id: term, name: term });
    return { id: term, name: term };
  };
}
