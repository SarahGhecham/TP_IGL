import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AcceuilAdComponent } from './acceuilAd.component';

describe('AcceuilComponent', () => {
  let component: AcceuilAdComponent;
  let fixture: ComponentFixture<AcceuilAdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AcceuilAdComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AcceuilAdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
