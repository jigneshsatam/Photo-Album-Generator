import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuestLandingComponent } from './guest-landing.component';

describe('GuestLandingComponent', () => {
  let component: GuestLandingComponent;
  let fixture: ComponentFixture<GuestLandingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GuestLandingComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GuestLandingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
