import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

interface SlideshowRouterState {
  images: any[];
}

@Component({
  selector: 'app-slideshow',
  templateUrl: './slideshow.component.html',
  styleUrls: ['./slideshow.component.sass']
})
export class SlideshowComponent implements OnInit {
  images: any[] = [];

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation && navigation.extras.state) {
      const state = navigation.extras.state as SlideshowRouterState;
      this.images = state.images;
    }
  }

  ngOnInit(): void {
  }
}
