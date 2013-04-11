var module_add_subscription = (function(){
	
	var init = function(){
		var import_div = $('<div id="module_add_subscription" />');
		$("#import").append(import_div);
		import_div=$("#module_add_subscription");
		
		import_div.load("/static/feed/add_subscription.html #add_subscription_import",function(){
			$("#show_add_subscription_modal_btn").click(show_add_subscription_modal_btn);
			$("#add_subscription_submit_btn").click(add_subscription_submit_btn);
		});
	}
	
	var show_add_subscription_modal_btn = function(){
		$("#add_subscription_url_input").val("");
	}
	
	var add_subscription_submit_btn = function(){
		input_url = $("#add_subscription_url_input").val();
		// $.ajax({
			// type: "POST",
			// dataType: "json",
			// url: "/feed/j_add_subscription/",
			// data: {
				// csrfmiddlewaretoken: $.cookie('csrftoken'),
				// url: input_url,
			// },
		// }).done(function(j){
			// console.log(JSON.stringify(j));
			// if(j.success){
				// var subscription_id = j.subscription.id;
				// $("#add_subscription_modal").modal("hide");
				// module_list_subscription.refresh(function(){
					// module_list_subscription.select(subscription_id,null);
				// });
			// }
		// });
		utils.remote(
			'add_subscription',
			{
				url: input_url,
			},
			function(j){
				console.log(JSON.stringify(j));
				if(j.success){
					var subscription_id = j.subscription.id;
					$("#add_subscription_modal").modal("hide");
					module_list_subscription.refresh(function(){
						module_list_subscription.select(subscription_id,null);
					});
				}
			}
		);
		// $("#add_subscription_modal").modal("hide");
	}
	
	return {
		init: init
	};
	
})();

$(module_add_subscription.init);
