import { TestBed } from '@angular/core/testing';

import { RadiologueService } from './radiologue.service';

describe('RadiologueService', () => {
  let service: RadiologueService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RadiologueService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
