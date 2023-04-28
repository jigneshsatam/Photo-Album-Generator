import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuestRegisterComponent } from './register-guest.component';

describe('GuestRegisterComponent', () => {
  let component: GuestRegisterComponent;
  let fixture: ComponentFixture<GuestRegisterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GuestRegisterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GuestRegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
