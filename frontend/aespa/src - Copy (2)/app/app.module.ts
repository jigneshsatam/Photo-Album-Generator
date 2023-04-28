import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GuestLoadImagesComponent } from './guest-load-images/guest-load-images.component';
import { LoadImagesComponent } from './load-images/load-images.component';
import { HeaderComponent } from './header/header.component';
import { AdminRegisterComponent } from './register-admin/register-admin.component';
import { GuestRegisterComponent } from './register-guest/register-guest.component';
import { LoginComponent } from './login/login.component';
import { ViewImagesComponent } from './view-images/view-images.component';
import { SlideshowComponent } from './slideshow/slideshow.component';
import { AdminLandingComponent } from './admin-landing/admin-landing.component';
import { GuestLandingComponent } from './guest-landing/guest-landing.component';
import { TaggingComponent } from './tagging/tagging.component';
import { UploadComponent } from './upload/upload.component';

import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
    AppComponent,
    GuestLoadImagesComponent,
    LoadImagesComponent,
    HeaderComponent,
    LoginComponent,
    AdminRegisterComponent,
    GuestRegisterComponent,
    ViewImagesComponent,
    SlideshowComponent,
    AdminLandingComponent,
    GuestLandingComponent,
    TaggingComponent,
    UploadComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule,
    NgSelectModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
