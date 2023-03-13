import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = 'aespa';

  // imageFile!: File;
  // imageUrl!: string;

  // onFileSelected(event: Event) {
  //   this.imageFile = (<HTMLInputElement>event.target).files![0];
  //   // this.imageFile = event.target.files[0];
  //   this.imageUrl = URL.createObjectURL(this.imageFile);
  // }


  message: string | undefined;
  imagePath: any;
  url: string | ArrayBuffer | null | undefined;

  // localUrl: string = 'file:///images/test.jpg';
  localUrl: string = "assets/uploads/images/test.jpg"

  // onInit() {

  // }

  onFileChanged(event: Event) {
    const files = (<HTMLInputElement>event.target).files;
    if (files!.length === 0)
      return;

    const mimeType = files![0].type;
    if (mimeType.match(/image\/*/) == null) {
      this.message = "Only images are supported.";
      return;
    }

    const reader = new FileReader();
    this.imagePath = files;
    // let img = new Image();

    reader.readAsDataURL(files![0]);
    // reader.readAsDataURL("assets/images/test.jpg");
    reader.onload = (_event) => {
      this.url = reader.result;
    }
  }

}
