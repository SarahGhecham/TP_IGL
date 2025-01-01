import { TestBed } from '@angular/core/testing';

import { AddConsultationService } from './add-consultation.service';

describe('AddConsultationService', () => {
  let service: AddConsultationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AddConsultationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
