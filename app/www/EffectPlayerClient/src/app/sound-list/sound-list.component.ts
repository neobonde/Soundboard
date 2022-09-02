import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild, ViewContainerRef } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { delay, retry } from 'rxjs';
import { ImgLoadService } from '../img-load.service';
import { LoadControlService } from '../load-control.service';
import { ModalUploadComponent } from '../modal-upload/modal-upload.component';
import { SoundCardComponent } from '../sound-card/sound-card.component';
import { SoundDirective } from '../sound.directive';

@Component({
  selector: 'app-sound-list',
  templateUrl: './sound-list.component.html',
  styleUrls: ['./sound-list.component.css']
})
export class SoundListComponent implements OnInit {

  @ViewChild(SoundDirective) soundList!: SoundDirective

  public loading = true;

  public sounds: any[] = []

  private timeout: any;

  constructor(private http: HttpClient, private imgLoader: ImgLoadService, private modalService: NgbModal, private loadService: LoadControlService) {
  }

  ngOnInit() {

    this.loadService.loadSoundsCalled$.subscribe(()=>{
      this.loadSounds();
    })

    this.loadService.loadSounds()

    this.imgLoader.imagesLoading$.subscribe(data => {
      if (data <= 1) {
        this.timeout = setTimeout(() => {
          clearTimeout(this.timeout);
          this.loading = false;
        }, 1000)
      }

      if (data > 1) {
        clearTimeout(this.timeout);
      }

      if (data <= 0) {
        clearTimeout(this.timeout);
        this.loading = false;
      } else {
        this.loading = true;
      }
    })

  }

  private loadSounds()
  {
    this.loading = true;
    this.http.get('/api/v1/get-sounds')
    .pipe(
      retry(3),
      delay(1000)
    ).subscribe(data => {
      this.sounds = data as []
      console.log(data)
      if (this.sounds.length == 0) {
        this.loading = false;
      }
    })
  }

  openUploadModal() {
    const modalRef = this.modalService.open(ModalUploadComponent);

    modalRef.componentInstance.fileUploaded.subscribe(()=>{
      this.loadService.loadSounds()
    });

  }


}
