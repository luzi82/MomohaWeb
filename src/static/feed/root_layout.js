var root_layout = (function(){
	
	var MIN_WIDTH = 640;
	var MIN_HEIGHT = 480;
	
	var HEADER_H = 48;
	var MENU_W = 240;
	
	var init = function(){
		$(window).resize(
			maintain
		);
		maintain();
	}
	
	var tmp=0;
	
	var maintain = function(){
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
		
		menu_x=0;
		menu_y=header_h;
		menu_w=MENU_W;
		menu_h=body_h-menu_y;

		content_x=menu_w;
		content_y=header_h;
		content_w=body_w-content_x;
		content_h=body_h-content_y;

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
		
		$('#menu').css({
			'left': menu_x,
			'top': menu_y,
			'width': menu_w,
			'height': menu_h,
		});
		
		$('#content').css({
			'left': content_x,
			'top': content_y,
			'width': content_w,
			'height': content_h,
		});
	};
	
	return {
		init: init,
		maintain: maintain
	};
	
})();

$(root_layout.init);
