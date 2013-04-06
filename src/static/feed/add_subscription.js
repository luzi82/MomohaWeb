var module_add_subscription = (function(){
	
	var init = function(){
		var import_div = $('<div id="module_add_subscription" />');
		$("#import").append(import_div);
		import_div=$("#module_add_subscription");
		
		import_div.load("/static/feed/add_subscription.html #add_subscription_import")
	}
	
	return {
		init: init
	};
	
})();

$(module_add_subscription.init);
