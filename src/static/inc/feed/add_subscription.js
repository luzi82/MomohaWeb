define([
	"jquery",
	"momohafeed",
], function(
	$
	, momohafeed
) {

// var module_add_subscription = (function(){
	
	var add_subscription_modal;
	
	var add_subscription_submit_btn;
	var add_subscription_close_btn;
	var add_subscription_url_input;
	var add_subscription_progress_bar;
	var add_subscription_progress;
	
	var busy = false;

	var init = function(){
		var import_div = $('<div id="module_add_subscription" />');
		$("#import").append(import_div);
		import_div=$("#module_add_subscription");
		
		import_div.load("inc/feed/add_subscription.html #add_subscription_import",function(){
			add_subscription_modal = $("#add_subscription_modal");
			
			add_subscription_submit_btn = $("#add_subscription_submit_btn");
			add_subscription_close_btn = $("#add_subscription_close_btn");
			add_subscription_url_input = $("#add_subscription_url_input");
			add_subscription_progress_bar = $("#add_subscription_progress_bar");
			add_subscription_progress = $("#add_subscription_progress");

			add_subscription_modal.on("hide",function(e){
				if(busy)e.preventDefault();
			});
			$("#show_add_subscription_modal_btn").click(show_add_subscription_modal_btn_click);
			add_subscription_submit_btn.click(add_subscription_submit_btn_click);
		});
	}
	
	var show_add_subscription_modal_btn_click = function(){
		if(busy)return;
		
		add_subscription_url_input.val("");
		add_subscription_submit_btn.removeClass("disabled");
		add_subscription_close_btn.removeClass("disabled");
		add_subscription_progress.hide();
		add_subscription_progress_bar.css("width","0%");
	}
	
	var add_subscription_submit_btn_click = function(){
		if(busy)return;
		
		var input_url = add_subscription_url_input.val();

		add_subscription_submit_btn.addClass("disabled");
		add_subscription_close_btn.addClass("disabled");
		add_subscription_progress_bar.css("width","30%");
		add_subscription_progress.show();

		busy = true;
		
		require([
			"feed_list_subscription"
		], function(
			feed_list_subscription
		) {
			var onFail = function(){
				busy = false;
				add_subscription_submit_btn.removeClass("disabled");
				add_subscription_close_btn.removeClass("disabled");
				add_subscription_progress_bar.css("width","0%");
			};
			
			momohafeed.add_subscription(input_url,function(j){
				if(j.success){
					add_subscription_progress_bar.css("width","60%");
					var subscription_id = j.subscription.id;
					feed_list_subscription.refresh(function(){
						add_subscription_progress_bar.css("width","90%");
						feed_list_subscription.select(subscription_id,function(){
							busy=false;
							add_subscription_modal.modal("hide");
						});
					});
				}else{
					onFail();
				}
			},onFail // TODO issue 104
			);
		});
	}

	init();	
	
	return {
		// init: init
	};

});

// })();
// 
// $(module_add_subscription.init);
