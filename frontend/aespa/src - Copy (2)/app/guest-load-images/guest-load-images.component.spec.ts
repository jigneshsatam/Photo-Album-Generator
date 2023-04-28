import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuestLoadImagesComponent } from './guest-load-images.component';

describe('GuestLoadImagesComponent', () => {
  let component: GuestLoadImagesComponent;
  let fixture: ComponentFixture<GuestLoadImagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GuestLoadImagesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GuestLoadImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
