var module_list_subscription = (function(){

	var init = function(){
		refresh();
	}
	
	var refresh = function(){
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
							console.log(subscription_id);
							module_subscription.load(subscription_id);
						});
						
					li.append(a);
				list_subscription_ul.append(li);
			}
		});
	}

	return {
		init: init,
		refresh: refresh
	}
	
})();

$(module_list_subscription.init);
