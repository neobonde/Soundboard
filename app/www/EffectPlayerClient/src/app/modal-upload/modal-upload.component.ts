import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-modal-upload',
  templateUrl: './modal-upload.component.html',
  styleUrls: ['./modal-upload.component.css']
})
export class ModalUploadComponent implements OnInit {

  @Output() fileUploaded: EventEmitter<any> = new EventEmitter();

  constructor(private http: HttpClient, public activeModal: NgbActiveModal) { }

  private soundFile: File | undefined;
  public soundTitle: string = ''
  public uploading: boolean = false;

  public fileValidClass = '';
  public titleValidClass = '';


  ngOnInit(): void {
  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;

    if (target.files && target.files.length) {
      console.log(target.files)
      this.soundFile = target.files[0];
      console.log(this.soundFile)
    }

  }

  upload() {
    this.uploading = true;

    if (this.soundTitle.length <= 0){
      this.titleValidClass = 'is-invalid'
    }else{
      this.titleValidClass = 'is-valid'
    }

    if (this.soundFile){
      this.fileValidClass = 'is-valid'
    }else{
      this.fileValidClass = 'is-invalid'
    }

    if (this.soundFile && this.soundTitle.length > 0) {

      const formData = new FormData();

      formData.append("file", this.soundFile);
      formData.append("title", this.soundTitle)

      const upload$ = this.http.post("/api/v1/upload", formData);
      upload$.subscribe(x=>{
        this.activeModal.close('Upload click')
        this.fileUploaded.emit();
      });

    }else
    {
      this.uploading = false;
    }

  }

}
