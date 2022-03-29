import { Directive, ElementRef, HostListener } from '@angular/core';
import { ImgLoadService as ImgLoadService } from './img-load.service';

@Directive({
  selector: 'img'
})
export class ImgLoadDirective {

  constructor(private el: ElementRef, private imageService :ImgLoadService) {
    imageService.imageLoading(el.nativeElement);
  }


  @HostListener('load')
  onLoad() {
    this.imageService.imageLoadedOrError(this.el.nativeElement);
  }

  @HostListener('error')
  onError() {
    this.imageService.imageLoadedOrError(this.el.nativeElement);
  }

}
