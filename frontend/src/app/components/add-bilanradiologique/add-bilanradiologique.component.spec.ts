import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddBilanradiologiqueComponent } from './add-bilanradiologique.component';

describe('AddBilanradiologiqueComponent', () => {
  let component: AddBilanradiologiqueComponent;
  let fixture: ComponentFixture<AddBilanradiologiqueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddBilanradiologiqueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddBilanradiologiqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
