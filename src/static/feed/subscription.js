var module_subscription = (function(){

	var load = function(subscription_id){
		
		subscription_list_item_table = $("#subscription_list_item_table");
		subscription_list_item_table.empty();
		
		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/feed/j_subscription_list_item/",
			data: {
				csrfmiddlewaretoken: $.cookie('csrftoken'),
				subscription_id: subscription_id,
			},
		}).done(function(j){
			console.log(JSON.stringify(j));
			for(i=0;i<j.item_list.length;++i){
				item = j.item_list[i];
				
				tr = $('<tr />');
				td = $('<td />');
				
					td.text(item.title);
				
				tr.append(td);
				subscription_list_item_table.append(tr);
			}
		});
		
	}

	return {
		load: load
	}
	
})();
