define([
	"jquery"
], function(
	$
) {

// var root_layout = (function(){
	
	var PHI = (1.0+Math.sqrt(5.0))/2.0;
	var PHI_1 = PHI-1;
	var PHI_2 = 2-PHI;
	
	var MIN_WIDTH = 640;
	var MIN_HEIGHT = 480;
	
	var HEADER_H = 40;
	var MENU_H = 48;
	var SUBSCRIPTION_LIST_AREA_W = 240;
	
	var PHIBOX_W_MIN = 640;
	var PHIBOX_H_MIN = Math.round(PHIBOX_W_MIN*PHI_1);
	
	var init = function(){
		$(window).resize(body_maintain);
		$("#list_subscription_area").resize(list_subscription_area_maintain);
		$("#subscription_area").resize(subscription_area_maintain);
		
		body_maintain();
	}
	
	var body_maintain = function(){
		window_w = $(window).width();
		window_h = $(window).height();
		
		if(window_w<MIN_WIDTH){
			body_w = MIN_WIDTH;
			body_scroll_x = 'scroll';
		}else{
			body_w = window_w;
			body_scroll_x = 'hidden';
		}
		if(window_h<MIN_HEIGHT){
			body_h = MIN_HEIGHT;
			body_scroll_y = 'scroll';
		}else{
			body_h = window_h;
			body_scroll_y = 'hidden';
		}
		
		header_x=0;
		header_y=0;
		header_w=body_w;
		header_h=HEADER_H;
		
		app_x=0;
		app_y=header_h;
		app_w=body_w;
		app_h=body_h-app_y;
		
		phibox_w = Math.max(PHIBOX_W_MIN, Math.round(app_w*PHI_2));
		phibox_h = Math.max(PHIBOX_H_MIN, Math.round(app_h*PHI_2));
		phibox_w = Math.min(phibox_w, Math.round(phibox_h*PHI));
		phibox_h = Math.min(phibox_h, Math.round(phibox_w*PHI_1));
		phibox_x = Math.round((app_w-phibox_w)/2);
		phibox_y = Math.round((app_h-phibox_h)*PHI_2);
		phibox_y = Math.max(phibox_y,0);
		
		phibox_form_divx = Math.round(phibox_w*PHI_2);
		phibox_form_label_w = phibox_form_divx-20;
		phibox_form_control_ml = phibox_form_divx;
		
		list_subscription_area_x=0;
		list_subscription_area_y=header_h;
		list_subscription_area_w=SUBSCRIPTION_LIST_AREA_W;
		list_subscription_area_h=body_h-list_subscription_area_y;

		subscription_area_x=list_subscription_area_w;
		subscription_area_y=header_h;
		subscription_area_w=body_w-subscription_area_x;
		subscription_area_h=body_h-subscription_area_y;

		$('body').css({
			'width': body_w,
			'height': body_h,
			'overflow-x': body_scroll_x,
			'overflow-y': body_scroll_y,
		});
		
		$('#header').css({
			'left': header_x,
			'top': header_y,
			'width': header_w,
			'height': header_h,
		});
		
		$('.app').css({
			'left': app_x,
			'top': app_y,
			'width': app_w,
			'height': app_h,
		});
		
		$('.phibox').css({
			'left': phibox_x,
			'top': phibox_y,
			'width': phibox_w,
			'height': phibox_h,
		});

		var phibox_Q = $('.phibox');
		var phibox_fh_Q = $('.form-horizontal',phibox_Q);
		$('.control-label',phibox_fh_Q).css({
			'width': phibox_form_label_w,
		});

		$('.controls',phibox_fh_Q).css({
			'margin-left': phibox_form_control_ml,
		});

		$('#list_subscription_area').css({
			'left': list_subscription_area_x,
			'top': list_subscription_area_y,
			'width': list_subscription_area_w,
			'height': list_subscription_area_h,
		});
		
		$('#subscription_area').css({
			'left': subscription_area_x,
			'top': subscription_area_y,
			'width': subscription_area_w,
			'height': subscription_area_h,
		});
		
		list_subscription_area_maintain();
		subscription_area_maintain();
	};
	
	var list_subscription_area_maintain = function(){
		area_maintain(
			$('#list_subscription_area'),
			$('#list_subscription_menu'),
			$('#list_subscription_main')
		);
	};
	
	var subscription_area_maintain = function(){
		area_maintain(
			$('#subscription_area'),
			$('#subscription_menu'),
			$('#subscription_main')
		);
	};
	
	var area_maintain = function(area, menu, main){
		
		area_w = area.width();
		area_h = area.height();
		
		menu_x = 0;
		menu_y = 0;
		menu_w = area_w;
		menu_h = MENU_H;
		
		main_x = 0;
		main_y = menu_h;
		main_w = area_w;
		main_h = area_h-main_y;
		
		menu.css({
			'left':  menu_x, 'top':    menu_y,
			'width': menu_w, 'height': menu_h,
		});
		main.css({
			'left':  main_x, 'top':    main_y,
			'width': main_w, 'height': main_h,
		});
	}
	
	var hide_mainarea = function(){
		$(".mainarea").hide();
	}
	
	init();
	
	return {
		body_maintain: body_maintain,
		// init: init,
		hide_mainarea: hide_mainarea,
	};
	
});
	
// })();

// $(root_layout.init);
