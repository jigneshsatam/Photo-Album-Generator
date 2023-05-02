import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.sass']
})
export class UploadComponent implements OnInit {
  selectedItem: { name: string; type: string } | null = null;
  showFileExplorer = false;
  folders = ['folder1', 'folder2', 'folder3'];
  files = ['file1.txt', 'file2.txt', 'file3.txt'];
  apiUrl = 'http://localhost:8827/images/GetSubDirAndFiles'
  //TODO: add stack to keep track of previous folders

  constructor(private http: HttpClient, private router: Router, private route: ActivatedRoute) { }

  ngOnInit(): void {
    const json = { "dirPath": "/" };
    const headers = { 'content-type': 'application/json' }

    this.http.post(this.apiUrl, json, { headers }
    ).subscribe((response: any) => {
      console.log(response.path);
      console.log(response);
      this.folders = response.Directories;
      this.files = response.Files;
    });
  }

  toggleFileExplorer(): void {
    this.showFileExplorer = !this.showFileExplorer;
    if (!this.showFileExplorer) {
      this.navigateTo('/');
    }
  }

  navigateTo(folder: string): void {
    var json = { "dirPath": folder };
    var headers = { 'content-type': 'application/json' }
    this.http.post(this.apiUrl, json, { headers }).subscribe((response: any) => {
      console.log(response.path);

      // Update folders and files based on the response
      this.folders = response.Directories;
      this.files = response.Files;
    });
  }

  // go to subdir
  selectItem(item: string, type: string): void {
    this.selectedItem = { name: item, type };
    console.log(`Selected item: ${this.selectedItem.name}, type: ${this.selectedItem.type}`);
  }

  onDoubleClick(item: string, type: string): void {
    this.selectedItem = { name: item, type };
    this.navigateTo(item)
  }

  // FINAL SELECT
  select(): void {
    if (!this.selectedItem) {
      console.log('No item selected');
      return;
    }

    var data = this.selectedItem.name;
    var post_url = 'http://localhost:8827/images/AddNewDirectory';
    var json = {
      "dirPath": this.selectedItem.name + '/',
      "userId": 1
    }

    // PASS THE path to the backend
    var headers = { 'content-type': 'application/json' }
    this.http.post(post_url, json, { headers, observe: 'response', responseType: 'json' }).subscribe((response: HttpResponse<any>) => {
      console.log(response);
      console.log(response.body)
      if (response.status == 200) {
        var dirID = response.body.directoryId
        this.router.navigate([`admin/${dirID}/load-images`], {
          state: { data: data },
        });
        // SEND THE PATH TO THE LOAD IMAGE COMPONENT
      }
      else {
        console.log("Error, could not add directory. status: " + response.status + ", status code: " + response.body.status + "");
      }
    });
  }

  cancel(): void {
    this.showFileExplorer = false;
  }
}
