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
  private stack: string[] = [];
  base_dir = "/app/uploads";
  current_dir = this.base_dir;
  subDirectories: boolean = true;

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

  updateCurrentDir(folder: string): void {
    if (folder === '/') {
      this.current_dir = this.base_dir;
      return;
    }
      this.current_dir = this.base_dir + "/" + folder;
    }

  push(folder: string): void {
    this.stack.push(folder);
  }

  pop(): string | undefined {
    return this.stack.pop();
  }

  stackIsEmpty(): boolean {
    return this.stack.length === 0;
  }

  toggleFileExplorer(): void {
    this.showFileExplorer = !this.showFileExplorer;
    if (!this.showFileExplorer) {
      this.navigateTo('/', false);
    }
  }

  navigateTo(folder: string, back: boolean): void {
    var json = { "dirPath": folder };
    var headers = { 'content-type': 'application/json' }
    this.http.post(this.apiUrl, json, { headers }).subscribe((response: any) => {
      //console.log(response.path);

      // Update folders and files based on the response
      this.folders = response.Directories;
      this.files = response.Files;
      if(folder != '/' && back == false){
        this.push(folder);
      }
      this.updateCurrentDir(folder);

      //if no subdirectories, alert
      if (this.folders.length == 0) {
      this.subDirectories = false;
      console.log("No subdirectories", this.subDirectories);
      }
      else {
        this.subDirectories = true;
        console.log("Subdirectories", this.subDirectories);
      }
    });
  }

  // go to subdir
  selectItem(item: string, type: string): void {
    this.selectedItem = { name: item, type };
    console.log(`Selected item: ${this.selectedItem.name}, type: ${this.selectedItem.type}`);
  }

  onDoubleClick(item: string, type: string): void {
    //this.selectedItem = null;
    this.navigateTo(item, false);
  }

  back(): void {
    if (this.stackIsEmpty()) {
      console.log('Already at root');
      return;
    }
    var elem = this.stack.pop();
    console.log("elem popped: ", elem);

    if (this.stackIsEmpty()) {
      console.log('At root')
      this.selectedItem = null;
      this.navigateTo('/', false);
    }
    else {
      console.log("stack after pop", this.stack);
      var back_url = this.stack[this.stack.length - 1];
      this.selectedItem = { name: back_url, type: 'folder'};
      console.log("THE URL TO GO TO IS: ", back_url)
      this.navigateTo(back_url, true);
    }

  }

  // FINAL SELECT
  select(): void {
    if (!this.selectedItem) {
      alert('No item selected');
      console.log('No item selected');
      return;
    }

    var data = this.selectedItem.name;
    var post_url = 'http://localhost:8827/images/AddNewDirectory';
    var json = {
      "dirPath": this.selectedItem.name + '/',
      "userId": 1
    }

    console.log("json: ", json);

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
    console.log('Cancel');
    this.stack = [];
    this.current_dir = this.base_dir;
    console.log(this.stack);
    console.log(this.current_dir);
  }
}
