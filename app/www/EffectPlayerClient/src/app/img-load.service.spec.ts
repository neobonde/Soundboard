import { TestBed } from '@angular/core/testing';

import { ImgLoadService } from './img-load-service.service';

describe('ImgLoadService', () => {
  let service: ImgLoadService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImgLoadService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
