import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[soundList]'
})
export class SoundDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
