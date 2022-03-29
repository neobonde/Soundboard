import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SoundControlsComponent } from './sound-controls.component';

describe('SoundControlsComponent', () => {
  let component: SoundControlsComponent;
  let fixture: ComponentFixture<SoundControlsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SoundControlsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SoundControlsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
