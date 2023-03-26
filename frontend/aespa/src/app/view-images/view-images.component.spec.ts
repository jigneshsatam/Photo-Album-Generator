import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewImagesComponent } from './view-images.component';

describe('ViewImagesComponent', () => {
  let component: ViewImagesComponent;
  let fixture: ComponentFixture<ViewImagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewImagesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
