import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatMenuTrigger } from '@angular/material/menu';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalDeleteComponent } from '../modal-delete/modal-delete.component';
import { ModalRenameComponent } from '../modal-rename/modal-rename.component';
import { VolumeControlService } from '../volume-control.service';

@Component({
  selector: 'app-sound-card',
  templateUrl: './sound-card.component.html',
  styleUrls: ['./sound-card.component.css']
})
export class SoundCardComponent implements OnInit {

  @Input() id = -1
  @Input() title = 'No title? 🤔';
  @Input() soundUri = '';
  @Input() thumbUri = '';

  @ViewChild(MatMenuTrigger, {static: true}) matMenuTrigger!: MatMenuTrigger;

  menuTopLeftPosition = {x: '0', y: '0'}


  constructor(private http: HttpClient, private volumeService: VolumeControlService, private modalService: NgbModal) { }

  ngOnInit(): void {
  }

  animate(): void {
    let ripple = document.createElement("span");
    ripple.classList.add("ripple")


  }

  playSound(): void {
    this.animate()
    this.http.post<any>('/api/v1/play', {volume:this.volumeService.volume.toString(), sound:this.soundUri}).subscribe(data => {
      console.log(data);
    })
  }

  onRightClick(event: MouseEvent): void
  {
    event.preventDefault();

    this.menuTopLeftPosition.x = event.clientX + 'px'
    this.menuTopLeftPosition.y = event.clientY + 'px'

    this.matMenuTrigger.menuData = {id: this.id};

    this.matMenuTrigger.openMenu();
  }

  openDeleteModal() {
    const modalRef = this.modalService.open(ModalDeleteComponent,{
      backdrop: 'static',
    });

    modalRef.componentInstance.id = this.id
    modalRef.componentInstance.title = this.title

    modalRef.componentInstance.fileUploaded.subscribe(()=>{
      // this.loadSounds() // TODO:
    });

  }

  openRenameModal() {
    const modalRef = this.modalService.open(ModalRenameComponent,{
      backdrop: 'static',
    });

    modalRef.componentInstance.id = this.id
    modalRef.componentInstance.title = this.title

    modalRef.componentInstance.fileUploaded.subscribe(()=>{
      // this.loadSounds() // TODO:
    });

  }

}
