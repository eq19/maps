/* set _blank for outside links */
$('.external-link').unbind('click');
$(document.links).filter(function() {
  var cond = 0;
  cond += (this.hostname.indexOf("eq19.com") === -1)? 1: 0;
  cond += (this.hostname.indexOf("github.io") === -1)? 1: 0; 
  cond += (this.hostname != window.location.hostname)? 1: 0;
  return cond == 3;
}).attr('target', '_blank')

