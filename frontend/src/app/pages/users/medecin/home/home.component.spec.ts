import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeMedComponent } from './home.component';

describe('HomeMedComponent', () => {
  let component: HomeMedComponent;
  let fixture: ComponentFixture<HomeMedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeMedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeMedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

