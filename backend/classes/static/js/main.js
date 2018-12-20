function main() {

  (function () {
     'use strict';
     
    	$('a.page-scroll').click(function() {
          if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
              $('html,body').animate({
                scrollTop: target.offset().top - 40
              }, 900);
              return false;
            }
          }
        });
  
  	
      // Show Menu on Book
      $(window).bind('scroll', function() {
          var navHeight = $(window).height() - 500;
          if ($(window).scrollTop() > navHeight) {
              $('.navbar-default').addClass('on');
          } else {
              $('.navbar-default').removeClass('on');
          }
      });
  
      $('body').scrollspy({ 
          target: '.navbar-default',
          offset: 80
      });
  
  	// Hide nav on click
    $(".navbar-nav li a").click(function (event) {
      // check if window is small enough so dropdown is created
      var toggle = $(".navbar-toggle").is(":visible");
      if (toggle) {
        $(".navbar-collapse").collapse('hide');
      }
    });
  
    	// Portfolio isotope filter
      $(window).load(function() {
          var $container = $('.portfolio-items');
          $container.isotope({
              filter: '*',
              animationOptions: {
                  duration: 750,
                  easing: 'linear',
                  queue: false
              }
          });
          $('.cat a').click(function() {
              $('.cat .active').removeClass('active');
              $(this).addClass('active');
              var selector = $(this).attr('data-filter');
              $container.isotope({
                  filter: selector,
                  animationOptions: {
                      duration: 750,
                      easing: 'linear',
                      queue: false
                  }
              });
              return false;
          });
  
      });
  	
      // Nivo Lightbox 
      $('.portfolio-item a').nivoLightbox({
              effect: 'slideDown',  
              keyboardNav: true,                            
      });
  
  }());


}
main();



function preRegister(class_name, el) {
    const url = "/register/preregister"

    student_first = "";
    student_last = "";
    student_age = "";
    email = "";
    phone = "";
    parent_first = "";
    parent_last = "";

    if (class_name == 'adult'){
        student_first = $("#adult_first").val();
        student_last = $("#adult_last").val();
        email = $("#adult_email").val();
        phone = $("#adult_phone").val();
    }
    else if (class_name == 'beginning'){
        student_first = $("#beginner_first").val();
        student_last = $("#beginner_last").val();
        student_age = $("#beginner_student_age").val();
        email = $("#beginner_parent_email").val();
        phone = $("#beginner_parent_phone").val();
        parent_first = $("#beginner_parent_first").val();
        parent_last = $("#beginner_parent_last").val();
    }
    else if (class_name == 'pre-ballet'){
        student_first = $("#pre_student_first").val();
        student_last = $("#pre_student_last").val();
        student_age = $("#pre_student_age").val();
        email = $("#pre_parent_email").val();
        phone = $("#pre_parent_phone").val();
        parent_first = $("#pre_parent_first").val();
        parent_last = $("#pre_parent_last").val();
    }

    data = { "student_first": student_first,
             "student_last": student_last,
             "student_age": student_age,
             "email": email,
             "phone": phone,
             "parent_first": parent_first,
             "parent_last": parent_last,
             "class_name": class_name };

   $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: function() {
        alert("Thank you for pre-registering!") 
        $('#adultBalletModal').modal('hide');
        $('#beginningBalletModal').modal('hide');
        $('#preBalletModal').modal('hide');
      }
   });
 
}

function rsvp(){
    url = "http://localhost:8000/rsvp";
    data = { "first_name": $("#rsvp_first").val(),
             "last_name": $("#rsvp_last").val(),
             "email": $("#rsvp_email").val(),
             "phone": $("#rsvp_phone").val(),
             "num_children": $("#rsvp_num").val() };

    $.ajax({ 
        type: "POST",
        url: url,
        data: data,
        success: function() {
          alert("Thank you for RSVPing to our free class. We will be sending out a friendly email reminding you of the event!");
          $('#freeClassModal').modal('hide');
        }
    });
}
