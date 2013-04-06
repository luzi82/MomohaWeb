var root_layout = (function(){
	
	var MIN_WIDTH = 640;
	var MIN_HEIGHT = 480;
	
	var HEADER_H = 40;
	var MENU_H = 48;
	var SUBSCRIPTION_LIST_AREA_W = 240;
	
	var init = function(){
		$(window).resize(body_maintain);
		$("#subscription_list_area").resize(subscription_list_area_maintain);
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
		
		subscription_list_area_x=0;
		subscription_list_area_y=header_h;
		subscription_list_area_w=SUBSCRIPTION_LIST_AREA_W;
		subscription_list_area_h=body_h-subscription_list_area_y;

		subscription_area_x=subscription_list_area_w;
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
		
		$('#subscription_list_area').css({
			'left': subscription_list_area_x,
			'top': subscription_list_area_y,
			'width': subscription_list_area_w,
			'height': subscription_list_area_h,
		});
		
		$('#subscription_area').css({
			'left': subscription_area_x,
			'top': subscription_area_y,
			'width': subscription_area_w,
			'height': subscription_area_h,
		});
		
		subscription_list_area_maintain();
		subscription_area_maintain();
	};
	
	var subscription_list_area_maintain = function(){
		area_maintain(
			$('#subscription_list_area'),
			$('#subscription_list_menu'),
			$('#subscription_list_main')
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
	
	return {
		init: init
	};
	
})();

$(root_layout.init);
