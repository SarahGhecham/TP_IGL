import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AffichetypeComponent } from './affichetype.component';

describe('AffichetypeComponent', () => {
  let component: AffichetypeComponent;
  let fixture: ComponentFixture<AffichetypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AffichetypeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AffichetypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
