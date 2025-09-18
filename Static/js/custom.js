(function ($) {
    "use strict";
    var $wn = $(window);
	
    $wn.on('load',function(){
		
		/***************
		 *  Preloader  *
		 ***************/
		var $element = $("#loading");
		$element.fadeOut(1000);
			
        /***************************
         *   Header Fixed  *
         ***************************/
        $wn.on('scroll',function(){
            if ($(this).scrollTop() > 1) {
                $('header').addClass("header-small");
            } else {
                $('header').removeClass("header-small");
            }
        });
    });
	
    /***************************
     *   Header Search  *
     ***************************/  
	$(".header_search_outer .icon-search-icon").on('click',function(){
    	$(".header_search").slideToggle();
	});
	
	 /****************
	 *   Couter up  *
	 ****************/
	var $element = $('.counter');
	if ($element.length > 0) {
		$element.counterUp({
			delay: 10,
			time: 1000
		});
	}

    /***********************
     *   Feature Carousel  *
     ***********************/
    $('.feature-slider').owlCarousel({
        loop: true,
        margin: 30,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 2
            },
            768: {
                items: 3
            }
        }
    });

    /***********************
     *   Trainers Carousel  *
     ***********************/
    $('.trainers-slider').owlCarousel({
        loop: true,
        margin: 30,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 2
            },
            768: {
                items: 4
            }
        }
    });

    
    /***********************
     *  Gallery Isotope  *
     ***********************/
    $('.gallery-outer ul.tabs li:first').addClass('active');
	$(".gallery-outer ul.tabs li span").on('click',function(){
        $('.gallery-outer ul.tabs li').removeClass('active');
        $(this).parent().addClass('active');
    });
    var $grid = $('.grid').isotope({
    itemSelector: '.element-item',
    layoutMode: 'fitRows',
    getSortData: {
    name: '.name',
    symbol: '.symbol',
    number: '.number parseInt',
    category: '[data-category]',
    weight: function( itemElem ) {
    	var weight = $( itemElem ).find('.weight').text();
   	 	return parseFloat( weight.replace( /[\(\)]/g, '') );
    }
    }
    });
	 
    // filter functions
    var filterFns = {
    // show if number is greater than 50
    numberGreaterThan50: function() {
    var number = $(this).find('.number').text();
    return parseInt( number, 10 ) > 50;
    },
    // show if name ends with -ium
    ium: function() {
    var name = $(this).find('.name').text();
    return name.match( /ium$/ );
    }
    };
    // bind filter button click
    $('.gallery-outer .tabs').on( 'click', 'span', function() {
    var filterValue = $( this ).attr('data-filter');
    // use filterFn if matches value
    filterValue = filterFns[ filterValue ] || filterValue;
    $grid.isotope({ filter: filterValue });
    });
	
	 setInterval(function(){ $grid.isotope(); }, 300);

    /***********************
     *  class Schedule Tabs  *
     ***********************/
    $('.classSch-outer .tab_container').hide();
    $('.classSch-outer .tab_container:first').show();
    $('.classSch-outer ul.tabs li:first').addClass('active');
	$(".classSch-outer ul.tabs li a").on('click',function(){
        $('.classSch-outer ul.tabs li').removeClass('active');
        $(this).parent().addClass('active');
        var currentTab = $(this).attr('href');
        $('.classSch-outer .tab_container').hide();
        $(currentTab).show();
        return false;
    });
    /***********************
     *  Flicker Box  *
     ***********************/
    var gallery = $('.flicker-box a').simpleLightbox();
    /***********************
     *  Our Gallery Box  *
     ***********************/
    var gallery = $('.gallery-list a').simpleLightbox();

    /***************************
     *   Scroll to top action  *
     ***************************/
    var $element = $('.scroll-top');
    $wn.on("scroll", function () {
        if ($(this).scrollTop() > 100) {
            $element.fadeIn();
        } else {
            $element.fadeOut();
        }
    });

    $element.on("click", function () {
        var $scrollElement = $("html, body");
        $scrollElement.animate({
            scrollTop: 0
        }, 600);
        return false;
    }); 
	
	 /****************************
	 *   Validate Contact Form  *
	 ****************************/
	var $form = $("#contactform");
	if ($form.length > 0) {
		
		$form.validate({
			rules: {
				name: {
					required: true,
					minlength: 3
				},
				  
				email: {
					required: true,
					email: true
				},
				phone: {
					required: true,
					number: true,
					minlength: 10
				} 
			},
			messages: {
				name: {
					required: "Please Enter Name",
					minlength: "Name must consist of at least 3 characters"
				},
				 
				email: {
					required: "Please provide an Email",
					email: "Please enter a valid Email"
				},
				phone: {
					required: "Please provide Phone Number",
					number: "Please enter only digits",
					minlength: "Phone Number must be atleast 10 Numbers"
				},
				 
			},

			submitHandler: function ($form) {
				//Send Booking Mail AJAX
				var formdata = jQuery("#contactform").serialize();
				jQuery.ajax({
					type: "POST",
					url: "contact_form/ajax-contact.php",
					data: formdata,
					dataType: 'json',
					async: false,
					success: function (data) {
						if (data.success) {
							jQuery('.msg')
								.removeClass('alert alert-danger alert-dismissible');
							jQuery('.msg')
								.addClass('alert alert-success alert-dismissible');
							jQuery('.msg')
								.text('Thank You, Your Message Has been Sent');
						} else {
							jQuery('.msg')
								.removeClass('alert alert-success alert-dismissible');
							jQuery('.msg')
								.addClass('alert alert-danger alert-dismissible');
							jQuery('.msg')
								.text('Error on Sending Message, Please Try Again');
						}

					},
					error: function (error) {
						jQuery('.msg')
							.removeClass('alert alert-success alert-dismissible');
						jQuery('.msg')
							.addClass('alert alert-danger alert-dismissible');
						jQuery('.msg')
							.text('Something Went Wrong');
					}

				});
			}
		});
	}
		
	/***************
	 *  Aos Animation  *
	 ***************/
	AOS.init();
	

})(jQuery);
