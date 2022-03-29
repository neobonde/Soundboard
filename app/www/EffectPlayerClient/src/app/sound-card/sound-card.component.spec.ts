import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SoundCardComponent } from './sound-card.component';

describe('SoundCardComponent', () => {
  let component: SoundCardComponent;
  let fixture: ComponentFixture<SoundCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SoundCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SoundCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
