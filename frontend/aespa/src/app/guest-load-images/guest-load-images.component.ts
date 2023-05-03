import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Image } from "./image";
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router'

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
  getImageUrl = "http://localhost:8827/images/load?directory=uploads/";
  getTagUrl = 'http://localhost:8827/tags/fetchTags';
  searchFilterUrl = 'http://localhost:8827/images/FetchImagesFromTags';
  images: Image[] = [];
  imgToLoad: number | null = null;

  constructor(private http: HttpClient, private fb: FormBuilder, private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
    this.getImageUrl = `http://localhost:8827/images/load`;
    this.getImages();
    this.getTags();
    this.heroForm = this.fb.group({
      selectedTagIds: [],
    });
  }

  getImages() {
    var url = "";
    url = this.getImageUrl;
    if (this.imgToLoad == null) {
      this.images = []
    }
    this.http.get<any>(url)
      .subscribe({
        next: (data) => {
          console.log(data);
          if (this.imgToLoad == null) {
            data["images"].map((element: Image) => element["path"] = "assets/" + element.path)
            this.images = data["images"];
          } else {
            var updatedImage: Image;
            data["images"].forEach((element: Image) => {
              if (element.photo_id == this.imgToLoad) {
                updatedImage = element;
              }
            });
            this.images.map((img: Image) => {
              if (img.photo_id == this.imgToLoad) {
                img = updatedImage;
              }
            })
          }
          // data["images"].forEach((element: Image) => {
          //   if (this.imgToLoad == null) {
          //     element["path"] = "assets/" + element.path;
          //     this.images.push(element);
          //   } else {
          //     this.images
          //   }
          // });
        },
        error: (error) => {
          console.log("getImages error: ", error);
        }
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

  searchFilter() {
    const numOfImgs = Number((<HTMLInputElement>document.getElementById("num-of-images")).value);
    if (!numOfImgs) {
      alert('Enter a Number of Photos');
      return;
    }
  
    if (this.heroForm.value.selectedTagIds.length === 0) {
      alert('Enter Tags in the Search Bar');
      return;
    }
  
    const payload = {
      "userId": 1,
      "tags": this.heroForm.value.selectedTagIds.map((tag: any) => tag.id),
      "numOfImgs": numOfImgs
    };
    console.log('payload ====> ', payload);
  
    this.http.post<any>(this.searchFilterUrl, payload).subscribe(
      (response: any) => {
        console.log('response ====> ', response);
        this.images = response.images;
      },
      (error) => {
        console.log('addTags error: ', error);
      }
    );
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

  onDone() {
    this.router.navigate(['../guest/slideshow/']);
  }

}
