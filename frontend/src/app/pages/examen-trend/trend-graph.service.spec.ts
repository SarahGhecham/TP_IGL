//trend-graph.service.spec.ts
import { TestBed } from '@angular/core/testing';

import { ExamenService } from './trend-graph.service';

describe('TrendGraphService', () => {
  let service: ExamenService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ExamenService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
