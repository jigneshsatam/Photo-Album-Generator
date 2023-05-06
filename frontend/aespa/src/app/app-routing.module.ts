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
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { AuthGuard } from './auth.guard';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register-admin', component: AdminRegisterComponent },
  { path: 'register-guest', component: GuestRegisterComponent },
  { path: 'admin', component: AdminLandingComponent, canActivate: [AuthGuard] },
  { path: 'admin/upload', component: UploadComponent, canActivate: [AuthGuard] },
  { path: 'admin/:id/load-images', component: LoadImagesComponent, canActivate: [AuthGuard] },
  { path: 'admin/add-to-slideshow', component: GuestLoadImagesComponent, canActivate: [AuthGuard] },
  { path: 'guest', component: GuestLandingComponent },
  { path: 'guest/view', component: ViewImagesComponent },
  { path: 'admin/slideshow', component: SlideshowComponent, canActivate: [AuthGuard] },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

