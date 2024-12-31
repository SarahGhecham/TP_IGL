//exame-trend.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExamenTrendsComponent } from './examen-trend.component';

describe('ExamenTrendComponent', () => {
  let component: ExamenTrendsComponent;
  let fixture: ComponentFixture<ExamenTrendsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExamenTrendsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExamenTrendsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
