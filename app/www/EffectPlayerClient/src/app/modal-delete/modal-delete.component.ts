import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { LoadControlService } from '../load-control.service';

@Component({
  selector: 'app-modal-delete',
  templateUrl: './modal-delete.component.html',
  styleUrls: ['./modal-delete.component.css']
})
export class ModalDeleteComponent implements OnInit {

  constructor(private http: HttpClient, public activeModal: NgbActiveModal, private loadService: LoadControlService) { }

  @Input() title = "Unknown file"
  @Input() id = -1

  ngOnInit(): void {
  }

  onDelete(): void
  {
    console.warn("Deleting \"" + this.title + "\"!")

    this.http.post<any>('/api/v1/delete', {sound:this.id}).subscribe(data => {
      this.activeModal.close('Sound deleted')
      this.loadService.loadSounds()
    })
  }
}
