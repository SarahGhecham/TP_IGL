import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddBilanbiologiqueComponent } from './add-bilanbiologique.component';

describe('AddBilanbiologiqueComponent', () => {
  let component: AddBilanbiologiqueComponent;
  let fixture: ComponentFixture<AddBilanbiologiqueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddBilanbiologiqueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddBilanbiologiqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
