import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Image } from "./image";
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router'
import { window } from 'rxjs';


@Component({
  selector: 'app-load-images',
  templateUrl: './load-images.component.html',
  styleUrls: ['./load-images.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LoadImagesComponent {
  dirID: string | null = ""
  heroForm: any;
  tags: any[] = [
  ];
  getImageUrl = "http://localhost:8827/images/load?directory=uploads/"
  getTagUrl = 'http://localhost:8827/tags/fetchTags';
  addTagUrl = 'http://localhost:8827/tagging/tag-all-images'
  deleteTagUrl = 'http://localhost:8827/tagging/delete-tag'
  images: Image[] = [];
  uploadRecieved = false;
  dataRecieved = "";
  imgToLoad: number | null = null;


  constructor(private http: HttpClient, private fb: FormBuilder, private router: Router, private route: ActivatedRoute) { }


  ngOnInit() {
    const dataReceived = history.state.data;

    this.dirID = this.route.snapshot.paramMap.get('id');
    this.getImageUrl = `http://localhost:8827/images/${this.dirID}/load`;
    // if (dataReceived) {
    //   console.log('Data received:', dataReceived);
    //   this.dataRecieved = dataReceived;
    //   this.uploadRecieved = true;
    // } else {
    //   console.log('No data received');
    //   this.uploadRecieved = false;
    // }

    // this.uploadRecieved = true;

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

  addTags() {
    const tags: any[] = [];
    if (this.heroForm.value.selectedTagIds.length) {
      this.heroForm.value.selectedTagIds.forEach((element: any) => {
        tags.push({
          "tag_id": element.id,
          "name": element.name
        })
      });
      const payload = {
        "dir_id": Number(this.dirID),
        "tags": tags,
      }

      console.log("payload ====> ", payload);

      this.http.post<any>(this.addTagUrl, payload).subscribe((data: any) => {
        // alert('Tags Added');
        this.heroForm.reset();
        this.getImages();

      }, error => this.heroForm.reset());
    } else {
      alert('no Tags Added');
    }
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
    this.router.navigate(['../admin/']);
  }

  removeTag(img_id: number, tag_id: number) {
    console.log("img_id", img_id, "tag_id", tag_id)
    this.http.delete<any>(this.deleteTagUrl, {
      body: {
        "photo_id": String(img_id),
        "tag_id": String(tag_id),
      }
    }).subscribe({
      next: (data: any) => {
        console.log(data);
        this.imgToLoad = img_id;
        this.getImages();
        this.imgToLoad = null;
      },
      error: (error) => {
        console.log("getImages error: ", error);
      }
    });
  }
}
