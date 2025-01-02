import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddExamenbiologiqueComponent } from './add-examenbiologique.component';

describe('AddExamenbiologiqueComponent', () => {
  let component: AddExamenbiologiqueComponent;
  let fixture: ComponentFixture<AddExamenbiologiqueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddExamenbiologiqueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddExamenbiologiqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
