import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router'
import { Image } from './image';

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
    this.getTags();
    this.heroForm = this.fb.group({
      selectedTagIds: [],
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
      (data: any) => {
        console.log('response ====> ', data);
    //  this.images = response.images;
        data["images"].forEach((element: Image) => {
          element["imagePath"] = "assets/" + element.imagePath
        }) 
        this.images = data["images"];
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
