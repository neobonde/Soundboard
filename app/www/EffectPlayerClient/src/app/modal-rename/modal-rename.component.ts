import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { LoadControlService } from '../load-control.service';

@Component({
  selector: 'app-modal-rename',
  templateUrl: './modal-rename.component.html',
  styleUrls: ['./modal-rename.component.css']
})
export class ModalRenameComponent implements OnInit {

  constructor(private http: HttpClient, public activeModal: NgbActiveModal, private loadService: LoadControlService) { }

  @Input() title = "Unknown file"
  @Input() id = -1

  public newTitle = ""

  ngOnInit(): void {
    this.newTitle = this.title
  }

  onRename(): void {
    console.log("renaming \"" + this.title + "\" to " + this.newTitle + "!")

    this.http.post<any>('/api/v1/rename', {sound:this.id, new_name:this.newTitle}).subscribe(data => {
      this.activeModal.close('Sound renamed')
      this.loadService.loadSounds()
    })
  }

}
