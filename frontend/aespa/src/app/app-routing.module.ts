import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoadImagesComponent } from './load-images/load-images.component';
import { GuestLoadImagesComponent } from './guest-load-images/guest-load-images.component';
import { AdminRegisterComponent } from './register-admin/register-admin.component';
import { GuestRegisterComponent } from './register-guest/register-guest.component';
import { LoginComponent } from './login/login.component';
import { ViewImagesComponent } from './view-images/view-images.component';
import { SlideshowComponent } from './slideshow/slideshow.component';
import { AdminLandingComponent } from './admin-landing/admin-landing.component';
import { GuestLandingComponent } from './guest-landing/guest-landing.component';
import { UploadComponent } from './upload/upload.component';

const routes: Routes = [
  { path: '', component: LoadImagesComponent },
  { path: 'register-admin', component: AdminRegisterComponent },
  { path: 'register-guest', component: GuestRegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminLandingComponent },
  { path: 'admin/upload', component: UploadComponent },
  { path: 'admin/:id/load-images', component: LoadImagesComponent },
  { path: 'guest/load-images', component: GuestLoadImagesComponent },
  { path: 'guest', component: GuestLandingComponent },
  { path: 'guest/view', component: ViewImagesComponent },
  { path: 'guest/slideshow', component: SlideshowComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
