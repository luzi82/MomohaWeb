define([
	"jquery",
	"feed_list_subscription",
], function(
	$
	, feed_list_subscription
) {

	var show = function(){
		$(".app").hide();
		$("#list_subscription_area").show();
		feed_list_subscription.refresh();
	};
	
	var hide = function(){
		$("#list_subscription_area").hide();
		$("#subscription_area").hide();
	};
	
	return {
		show: show,
		hide: hide,
	};

});
