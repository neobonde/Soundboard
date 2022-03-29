import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadControlService {

  constructor() { }

  private loadSoundsSource = new Subject<any>();

  loadSoundsCalled$ = this.loadSoundsSource.asObservable();

  loadSounds() {
    this.loadSoundsSource.next(null);
  }


}
