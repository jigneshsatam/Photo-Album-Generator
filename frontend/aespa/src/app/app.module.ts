import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoadImagesComponent } from './load-images/load-images.component';
import { HeaderComponent } from './header/header.component';
import { LoginComponent } from './login/login.component';
import { ViewImagesComponent } from './view-images/view-images.component';
import { SlideshowComponent } from './slideshow/slideshow.component';
import { AdminLandingComponent } from './admin-landing/admin-landing.component';
import { GuestLandingComponent } from './guest-landing/guest-landing.component';
import { TaggingComponent } from './tagging/tagging.component';
import { UploadComponent } from './upload/upload.component';

@NgModule({
  declarations: [
    AppComponent,
    LoadImagesComponent,
    HeaderComponent,
    LoginComponent,
    ViewImagesComponent,
    SlideshowComponent,
    AdminLandingComponent,
    GuestLandingComponent,
    TaggingComponent,
    UploadComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
