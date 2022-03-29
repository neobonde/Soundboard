import { TestBed } from '@angular/core/testing';

import { LoadControlService } from './load-control.service';

describe('LoadControlService', () => {
  let service: LoadControlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoadControlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
