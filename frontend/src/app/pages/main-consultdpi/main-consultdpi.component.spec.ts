import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainConsultdpiComponent } from './main-consultdpi.component';

describe('MainConsultdpiComponent', () => {
  let component: MainConsultdpiComponent;
  let fixture: ComponentFixture<MainConsultdpiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MainConsultdpiComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MainConsultdpiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
