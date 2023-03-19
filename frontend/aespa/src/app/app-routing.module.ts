import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoadImagesComponent } from './load-images/load-images.component';

const routes: Routes = [
  { path: 'admin/load-images', component: LoadImagesComponent },
  { path: '', component: LoadImagesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
