import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SoundCardComponent } from './sound-card/sound-card.component';
import { SoundListComponent } from './sound-list/sound-list.component';
import { SoundControlsComponent } from './sound-controls/sound-controls.component';
import { SoundDirective } from './sound.directive';
import { ImgLoadDirective } from './img-load.directive';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatRippleModule } from '@angular/material/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ModalUploadComponent } from './modal-upload/modal-upload.component';
import {MatMenuModule} from '@angular/material/menu';
import {MatIconModule} from '@angular/material/icon';
import { ModalRenameComponent } from './modal-rename/modal-rename.component';
import { ModalDeleteComponent } from './modal-delete/modal-delete.component';



@NgModule({
  declarations: [
    AppComponent,
    SoundCardComponent,
    SoundListComponent,
    SoundControlsComponent,
    SoundDirective,
    ImgLoadDirective,
    ModalUploadComponent,
    ModalRenameComponent,
    ModalDeleteComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatRippleModule,
    NgbModule,
    MatMenuModule,
    MatIconModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
