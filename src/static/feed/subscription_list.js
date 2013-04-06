var module_subscription_list = (function(){

	var init = function(){
		refresh();
	}
	
	var refresh = function(){
		subscription_list_ul = $('#subscription_list_ul');
		subscription_list_ul.empty();
		
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
						
						a.click(function(){
							console.log(subscription.id);
						});
						
					li.append(a);
				subscription_list_ul.append(li);
			}
		});
	}

	return {
		init: init,
		refresh: refresh
	}
	
})();

$(module_subscription_list.init);
