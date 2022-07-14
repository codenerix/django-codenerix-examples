/**
 Core Shop layout handlers and wrappers
 **/

// BEGIN: Layout Brand
var LayoutQtySpinner = function () {

	return {
		//main function to initiate the module
		init: function () {
			$('.c-spinner .btn:first-of-type').on('click', function () {
				var data_input = $(this).attr('data_input');
				$('.c-spinner input.' + data_input).val(parseInt($('.c-spinner input.' + data_input).val(), 10) + 1);
			});

			$('.c-spinner .btn:last-of-type').on('click', function () {
				var data_input = $(this).attr('data_input');
				if ($('.c-spinner input.' + data_input).val() != 0) {
					$('.c-spinner input.' + data_input).val(parseInt($('.c-spinner input.' + data_input).val(), 10) - 1);
				}
			});
		}

	};
}();
// END

// BEGIN: Layout Checkbox Visibility Toggle
var LayoutCheckboxVisibilityToggle = function () {

	return {
		//main function to initiate the module
		init: function () {
			$('.c-toggle-hide').each(function () {
				var $checkbox = $(this).find('input.c-check'),
					$speed = $(this).data('animation-speed'),
					$object = $('.' + $(this).data('object-selector'));

				$object.hide();

				if (typeof $speed === 'undefined') {
					$speed = 'slow';
				}

				$($checkbox).on('change', function () {
					if ($($object).is(':hidden')) {
						$($object).show($speed);
					} else {
						$($object).slideUp($speed);
					}
				});
			});
		}
	};

}();
// END

// BEGIN: Layout Shipping Calculator
var LayoutShippingCalculator = function () {

	return {
		//main function to initiate the module
		init: function () {
			var $shipping_calculator = $('.c-shipping-calculator'),
				$radio_name = $($shipping_calculator).data('name'),
				$total_placeholder = $($shipping_calculator).data('total-selector'),
				$subtotal_placeholder = $($shipping_calculator).data('subtotal-selector'),
				$subtotal = parseFloat($('.' + $subtotal_placeholder).text());

			$('input[name=' + $radio_name + ']', $shipping_calculator).on('change', function () {
				var $price = $('input[name=' + $radio_name + ']:checked', $shipping_calculator).attr('logic');
				var price = JSON.parse($price);
				var price_transport = undefined;
				$.each(price, function(key, value){
					if ($subtotal <= value[0] && value[0] != null && price_transport == undefined){
						price_transport = value[1];
					}else if (value[0] == null && price_transport == undefined){
						price_transport = value[1];
					}
				});
				if (price_transport == undefined){
					price_transport = 0;
				}
				var $overall_total = $subtotal + price_transport;
				$('.' + $total_placeholder).text($overall_total.toFixed(2));
			});
		}
	};

}();
// END

// PRODUCT GALLERY
var LayoutProductGallery = function () {
	return {
		//main function to initiate the module
		init: function () {
			$('.c-product-gallery-content .c-zoom').toggleClass('c-hide'); // INIT FUNCTION - HIDE ALL IMAGES

			// SET GALLERY ORDER
			var i = 1;
			$('.c-product-gallery-content .c-zoom').each(function(){
				$(this).attr('img_order', i);
				i++;
			});

			// INIT ZOOM MASTER PLUGIN
			$('.c-zoom').each(function(){
				$(this).zoom();
			});

			// ASSIGN THUMBNAIL TO IMAGE
			var i = 1;
			$('.c-product-thumb img').each(function(){
				$(this).attr('img_order', i);
				i++;
			});

			// INIT FIRST IMAGE
			$('.c-product-gallery-content .c-zoom[img_order="1"]').toggleClass('c-hide');

			// CHANGE IMAGES ON THUMBNAIL CLICK
			$('.c-product-thumb img').click(function(){
				var img_target = $(this).attr('img_order');

				$('.c-product-gallery-content .c-zoom').addClass('c-hide');
				$('.c-product-gallery-content .c-zoom[img_order="'+img_target+'"]').removeClass('c-hide');
			});
        
        	// SET THUMBNAIL HEIGHT
        	var thumb_width = $('.c-product-thumb').width();
        	$('.c-product-thumb').height(thumb_width);

	    }
	}
}();

// BEGIN: Price Slider
var PriceSlider = function () {

	return {
		//main function to initiate the module
		init: function () {
			$('.c-price-slider').slider();
		}

	};

}();
// END

// Main theme initialization
$(document).ready(function () {
	// init layout handlers
	LayoutQtySpinner.init();
	LayoutCheckboxVisibilityToggle.init();
	LayoutShippingCalculator.init();
	LayoutProductGallery.init();
	PriceSlider.init();
});