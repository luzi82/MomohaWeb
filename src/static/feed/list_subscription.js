var module_list_subscription = (function(){

	var init = function(){
		refresh(null);
	}
	
	var refresh = function(done_callback){
		list_subscription_ul = $('#list_subscription_ul');
		list_subscription_ul.empty();
		
		$.ajax({
			dataType: "json",
			url: "/feed/j_list_subscription/",
		}).done(function(j){
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
			utils.cb(done_callback);
		});
	}
	
	var select = function(subscription_id,done_callback){
		console.log("select "+subscription_id);
		module_subscription.load(subscription_id,done_callback);
	}

	return {
		init: init,
		refresh: refresh,
		select: select,
	}
	
})();

$(module_list_subscription.init);
