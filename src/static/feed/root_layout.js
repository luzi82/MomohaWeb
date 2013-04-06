var root_layout = (function(){
	
	var MIN_WIDTH = 640;
	var MIN_HEIGHT = 480;
	
	var HEADER_H = 36;
	var SUBSCRIPTION_LIST_AREA_W = 240;
	
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
	};
	
	return {
		init: init,
		maintain: maintain
	};
	
})();

$(root_layout.init);
