var isToggled = false;
function toggleLanguage(){
  $('#footer_toggle').animate({'bottom': (isToggled ? '30px' : '70px')});
  isToggled = !isToggled;
  $('#language_footer').slideToggle();
}
