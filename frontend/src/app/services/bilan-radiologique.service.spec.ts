import { TestBed } from '@angular/core/testing';

import { BilanRadiologiqueService } from './bilan-radiologique.service';

describe('BilanRadiologiqueService', () => {
  let service: BilanRadiologiqueService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BilanRadiologiqueService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
