$( document ).ready(function() {
  $(".dropdown-trigger").dropdown();
  $('.sidenav').sidenav();
  $('.collapsible').collapsible();

  $("#search").on("keyup", function(e) {
    if (e.which == 27) {  // catch ESC key and clear input
      $(this).val('');
    }
    var value = $(this).val().toLowerCase();
    $("#menu-fields li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});