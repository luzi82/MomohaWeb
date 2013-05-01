define([
	"jquery",
	"momohafeed",
	"feed_utils",
], function(
	$
	, momohafeed
	, feed_utils
) {
	
	var refresh = function(done_callback){
		var list_subscription_ul = $('#list_subscription_ul');
		list_subscription_ul.empty();

		momohafeed.list_subscription(function(j){
			console.log(JSON.stringify(j));

			var tag_dict_dict={};			
			var tagged_subscription_list=[];
			
			for(var i=0;i<j.subscriptiontag_list.length;++i){
				var subscriptiontag = subscriptiontag_list[i];
				tag_dict_dict[tag.id]={
					title: subscriptiontag.title,
					subscription_list: [],
				}
			}
			
			for(var i=0;i<j.subscription_tag_list;++i){
				var subscription_tag = subscription_tag_list[i];
				tag_dict_dict[subscription_tag.tag_id].subscription_list.push(subscription_tag.subscription_id);
				tagged_subscription_list.push(subscription_tag.subscription_id);
			}
			
			console.log(tag_dict_dict);
			
			// for(var k in tag_dict_dict){
				// console.log(k);
				// var tag_dict=tag_dict_dict[k];
				// for(var i in )
			// }
			
			for(var i=0;i<j.subscription_list.length;++i){
				var subscription = j.subscription_list[i];

				// TODO issue 115
				var li = $('#list_subscription_li_template').clone();
					$('.list_subscription_title',li).text(subscription.title);
					var a=$('.list_subscription_a',li);
						a.data("subscription_id",subscription.id)
						a.click(function(){
							subscription_id = $(this).data("subscription_id");
							select(subscription_id,null);
						});
				list_subscription_ul.append(li);
			}
			feed_utils.cb(done_callback);
		},null); // TODO issue 96
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
	
	return {
		refresh: refresh,
		select: select,
	}
	
});
	
// })();
// 
// $(module_list_subscription.init);
