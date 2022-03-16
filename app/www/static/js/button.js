var buttons = document.getElementsByClassName('button');

Array.prototype.forEach.call(buttons, function(b){
  b.addEventListener('click', createRipple);
})

function createRipple(e)
{
  let ripples = this.getElementsByClassName('ripple')
  if(ripples.length > 0)
  {
    ripples[0].remove();
  }

  var circle = document.createElement('div');
  this.appendChild(circle);

  var d = Math.max(this.clientWidth, this.clientHeight);
  circle.style.width = circle.style.height = d + 'px';

  circle.style.left = e.clientX - this.offsetLeft - d / 2 + 'px';
  circle.style.top = e.clientY - this.offsetTop - d / 2 + 'px';

  circle.classList.add('ripple');
}
