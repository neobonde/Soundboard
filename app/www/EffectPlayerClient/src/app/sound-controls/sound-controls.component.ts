import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { VolumeControlService } from '../volume-control.service';


@Component({
  selector: 'app-sound-controls',
  templateUrl: './sound-controls.component.html',
  styleUrls: ['./sound-controls.component.css']
})
export class SoundControlsComponent implements OnInit {

  constructor(public volumeService: VolumeControlService, private http: HttpClient) { }

  ngOnInit(): void {

  }

  stopAll(): void {
    this.http.post<null>('/api/v1/stop', null).subscribe(data => {
      console.log(data);
    })
  }

  tvOff(): void {
    this.http.post<null>('/api/v1/tv_off', null).subscribe(data => {
      console.log(data);
    })
  }

  tvOn(): void {
    this.http.post<null>('/api/v1/tv_on', null).subscribe(data => {
      console.log(data);
    })
  }

}
