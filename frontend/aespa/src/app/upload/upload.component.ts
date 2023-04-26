import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.sass']
})
export class UploadComponent implements OnInit {
  selectedItem: { name: string; type: string } | null = null;
  showFileExplorer = false;
  folders = ['folder1', 'folder2', 'folder3']; // Replace this with your folder names
  files = ['file1.txt', 'file2.txt', 'file3.txt']; // Replace this with your file names

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  toggleFileExplorer(): void {
    this.showFileExplorer = !this.showFileExplorer;
  }

  navigateTo(folder: string): void {
    this.http.get(`http://localhost:5000/api/folder-path?folder=${folder}`).subscribe((response: any) => {
      console.log(response.path);
  
      // Mock API response
      const mockResponse = {
        folders: ['subfolder1', 'subfolder2', 'subfolder3'],
        files: ['file4.txt', 'file5.txt', 'file6.txt']
      };
  
      // Update folders and files based on the response
      this.folders = mockResponse.folders;
      this.files = mockResponse.files;
    });
  }


  selectItem(item: string, type: string): void {
    this.selectedItem = { name: item, type };
  }
  
  select(): void {
    if (!this.selectedItem) {
      console.log('No item selected');
      return;
    }

    console.log(`Selected item: ${this.selectedItem.name}, type: ${this.selectedItem.type}`);
    // Use the selected item's path and type as needed
  }

  cancel(): void {
    this.showFileExplorer = false;
  }
}
