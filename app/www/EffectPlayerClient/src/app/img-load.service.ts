import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ImgLoadService {
  private _imageLoading = new Subject<number>();
  private images: Map<HTMLElement, boolean> = new Map();
  private imagesLoading = 0;

  imagesLoading$ = this._imageLoading.asObservable();

  imageLoading(img: HTMLElement) {
    if (!this.images.has(img) || this.images.get(img)) {
      this.images.set(img,false);
      this.imagesLoading ++;
      this._imageLoading.next(this.imagesLoading);
    }
    // console.info('loading - ' + this.imagesLoading)
  }

  imageLoadedOrError(img: HTMLElement) {
    if(this.images.has(img) && !this.images.get(img))
    {
      this.images.set(img, true);
      this.imagesLoading--;
      this._imageLoading.next(this.imagesLoading);
    }
    // console.info('loaded - ' + this.imagesLoading)
  }

}
