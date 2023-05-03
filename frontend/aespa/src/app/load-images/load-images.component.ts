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
  images: Image[] = [];
  uploadRecieved = false;
  dataRecieved = "";


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
    // if (!this.uploadRecieved) {
    // }
    // else {
    //   // url = 'http://localhost:8827/images/load?directory=uploads/' + this.dataRecieved;
    //   // console.log("url: ", url);
    // }
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
        alert('Tags Added');
        // this.heroForm.reset()
        location.reload();

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
}
