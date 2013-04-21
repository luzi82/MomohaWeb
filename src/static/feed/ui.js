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
	
	return {
		show: show,
	};

});
