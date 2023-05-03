import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Image } from "./image";
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-load-images',
  templateUrl: './load-images.component.html',
  styleUrls: ['./load-images.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LoadImagesComponent {
  heroForm: any;
  tags: any[] = [
  ];
  apiUrl = 'http://localhost:8827/images/load?directory=uploads/images';
  images: Image[] = [];
  uploadRecieved = false;
  dataRecieved = "";


  constructor(private http: HttpClient, private fb: FormBuilder, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    const dataReceived = history.state.data;

    if (dataReceived) {
      console.log('Data received:', dataReceived);
      this.dataRecieved = dataReceived;
      this.uploadRecieved = true;
    } else {
      console.log('No data received');
      this.uploadRecieved = false;
    }

    this.getImages();
    this.heroForm = this.fb.group({
      selectedTagIds: [],
    });
  }

  getImages() {
    var url = "";
    if(!this.uploadRecieved) {
      url = this.apiUrl;
    }
    else {
      url = 'http://localhost:8827/images/load?directory=uploads/' + this.dataRecieved;
      console.log("url: ", url);
    }
    this.http.get<any>(url)
      .subscribe((data: any) => {
        console.log(data);
        data["images"].forEach((element: Image) => {
          element["path"] = "assets/" + element.path;
          this.images.push(element);
        });

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
    this.tags = this.tags.concat({ value: term, text: term });
    return { value: term, text: term };
  };
}
