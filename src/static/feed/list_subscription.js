define([
	"jquery",
	"momohafeed",
	"feed_utils",
], function(
	$
	, momohafeed
	, feed_utils
) {

// var module_list_subscription = (function(){

	// var init = function(){
		// refresh(null);
	// }
	
	var refresh = function(done_callback){
		list_subscription_ul = $('#list_subscription_ul');
		list_subscription_ul.empty();

		momohafeed.list_subscription(function(j){
			console.log(JSON.stringify(j));
			for(i=0;i<j.subscription_list.length;++i){
				subscription = j.subscription_list[i];

				li = $('<li />');
					a = $('<a />');
						a.text(subscription.title);
						a.attr('href',"#");
						a.data("subscription_id",subscription.id)
						
						a.click(function(){
							subscription_id = $(this).data("subscription_id");
							select(subscription_id,null);
						});
						
					li.append(a);
				list_subscription_ul.append(li);
			}
			feed_utils.cb(done_callback);
		});
	}
	
	var select = function(subscription_id,done_callback){
		require([
			"feed_subscription",
		], function(
			feed_subscription
		) {
			console.log("select "+subscription_id);
			feed_subscription.load(subscription_id,done_callback);
		});
	}
	
	// init();

	return {
		// init: init,
		refresh: refresh,
		select: select,
	}
	
});
	
// })();
// 
// $(module_list_subscription.init);
