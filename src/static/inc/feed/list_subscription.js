define([
	"jquery",
	"momohafeed",
	"feed_utils",
], function(
	$
	, momohafeed
	, feed_utils
) {

	var instance = null;
	
	var create_instance = function(){
		return {
			tag_dict_dict: null,
			subscription_dict_dict: null,
		};
	};
	
	var refresh = function(done_callback){
		var list_subscription_ul = $('#list_subscription_ul');
		list_subscription_ul.empty();
		
		instance = create_instance();

		momohafeed.list_subscription(function(j){
			console.log(JSON.stringify(j));

			instance.tag_dict_dict={};
			instance.subscription_dict_dict={};
			
			for(var i=0;i<j.subscriptiontag_list.length;++i){
				var subscriptiontag = j.subscriptiontag_list[i];
				instance.tag_dict_dict[subscriptiontag.id]={
					title: subscriptiontag.title,
					subscription_list: [],
				}
			}

			for(var i=0;i<j.subscription_list.length;++i){
				var subscription = j.subscription_list[i];
				instance.subscription_dict_dict[subscription.id]={
					title: subscription.title,
					tag_list: [],
				}
			}
			
			for(var i=0;i<j.subscriptiontagsubscriptionrelation_list.length;++i){
				var subscriptiontagsubscriptionrelation = j.subscriptiontagsubscriptionrelation_list[i];
				var subscriptiontag_id = subscriptiontagsubscriptionrelation.subscriptiontag_id;
				var subscription_id = subscriptiontagsubscriptionrelation.subscription_id;
				instance.tag_dict_dict[subscriptiontag_id].subscription_list.push(subscription_id);
				instance.subscription_dict_dict[subscription_id].tag_list.push(subscriptiontag_id);
			}
			
			for(var k in instance.tag_dict_dict){
				var tag_dict = instance.tag_dict_dict[k];
				
				// TODO issue 115
				var li = $('#list_subscription_tag_li_template').clone();
					$('.list_subscription_title',li).text(tag_dict.title);
					// var a=$('.list_subscription_a',li);
						// a.data("subscription_id",subscription.id)
						// a.click(function(){
							// subscription_id = $(this).data("subscription_id");
							// select(subscription_id,null);
						// });
				list_subscription_ul.append(li);
				
				for(var i=0;i<tag_dict.subscription_list.length;++i){
					var subscription_id = tag_dict.subscription_list[i];
					var subscription = instance.subscription_dict_dict[subscription_id];
					
					var li = $('#list_subscription_li_template').clone();
						$('.list_subscription_title',li).text(subscription.title);
						var a=$('.list_subscription_a',li);
							a.data("subscription_id",subscription_id)
							a.click(function(){
								var subscription_id = $(this).data("subscription_id");
								select(subscription_id,null);
							});
					list_subscription_ul.append(li);
				}
			}
			
			list_subscription_ul.append(
				$("#list_subscription_divider_li_template").clone()
			);
			
			for(var subscription_id in instance.subscription_dict_dict){
				var subscription_dict = instance.subscription_dict_dict[subscription_id];
				if(subscription_dict.tag_list.length>0)
					continue;

				// TODO issue 115
				var li = $('#list_subscription_li_template').clone();
					$('.list_subscription_title',li).text(subscription_dict.title);
					var a=$('.list_subscription_a',li);
						a.data("subscription_id",subscription_id)
						a.click(function(){
							var subscription_id = $(this).data("subscription_id");
							select(subscription_id,null);
						});
				list_subscription_ul.append(li);
			}
			feed_utils.cb(done_callback);
		},null); // TODO issue 96
	};
	
	var select = function(subscription_id,done_callback){
		require([
			"feed_subscription",
		], function(
			feed_subscription
		) {
			console.log("select "+subscription_id);
			feed_subscription.load(subscription_id,done_callback);
		});
	};
	
	var get_instance = function(){
		return instance;
	};
	
	return {
		get_instance: get_instance,
		refresh: refresh,
		select: select,
	};
	
});
	
// })();
// 
// $(module_list_subscription.init);
