var module_subscription = (function(){
	
	var subscription_instance = null;
	
	var init = function(){
		subscription_poll_btn = $("#subscription_poll_btn");
		subscription_poll_btn.click(function(){
			if(subscription_instance==null)
				return;

			module_momohafeed.subscription_poll(
				subscription_instance.subscription_id,
				function(j){
					load(subscription_instance.subscription_id,null);
				}
			);
		});

		var subscription_all_readdone_btn = $("#subscription_all_readdone_btn");
		subscription_all_readdone_btn.click(function(){
			if(subscription_instance==null)
				return;

			module_momohafeed.subscription_all_readdone(
				subscription_instance.subscription_id,
				function(j){
					load(subscription_instance.subscription_id,null);
				}
			);
		});
	}

	var load = function(subscription_id,done_callback){
		
		subscription_instance = {
			subscription_id: subscription_id,
			opening_row_id: null,
			vm_item_detail_list: null,
			row_data_dict: {},
		};
		
		subscription_list_item_table = $("#subscription_list_item_table");
		subscription_list_item_table.empty();
		
		// $.ajax({
			// type: "POST",
			// dataType: "json",
			// url: "/feed/j_subscription_list_item_detail/",
			// data: {
				// csrfmiddlewaretoken: $.cookie('csrftoken'),
				// subscription_id: subscription_id,
			// },
		// }).done(
		module_momohafeed.subscription_list_item_detail(
			subscription_id,
			function(j){
				console.log(JSON.stringify(j));
				subscription_instance.vm_item_detail_list = j.item_detail_list;
				for(var i=0;i<j.item_detail_list.length;++i){
					var item = j.item_detail_list[i];
					
					subscription_instance.row_data_dict[i]={
						vm_item: item,
						readdone: (item["readdone"]!=0),
					}
					
					tr_brief = $('<tr />');
						tr_brief.attr("id","subscription_list_item_row_"+i+"_brief");
						tr_brief.data("row_id",i);
						tr_brief.data("item_id",item.id);
						tr_brief.css("cursor","pointer");
						td = $('<td />');
						
							td.text(item.title);
						
						tr_brief.append(td);
					subscription_list_item_table.append(tr_brief);
					
					tr_detail = $('<tr />');
						tr_detail.attr("id","subscription_list_item_row_"+i+"_detail");
						tr_detail.data("row_id",i);
						tr_detail.css("display","none");
						td = $('<td />');
						
							title = $("<h4 />");
							title.text(item.title);
							title.css("cursor","pointer");
							title.data("row_id",i);
							td.append(title);
							
							d_content = $("<div />");
							d_content.html(item.content);
							d_content.css("margin-bottom","10px");
							td.append(d_content);
							
							d_share = $("<div />");
								share_btn = $("<img />")
									share_btn.data("link",item.link);
									share_btn.data("title",item.title);
									share_btn.attr({
										"class":"subscription_share_btn",
										"src":"/static/feed/img/share/facebook-16.png",
									});
									share_btn.click(function(){
										module_share.share_facebook($(this).data("link"),$(this).data("title"));
									});
								d_share.append(share_btn);
								share_btn = $("<img />")
									share_btn.data("link",item.link);
									share_btn.data("title",item.title);
									share_btn.attr({
										"class":"subscription_share_btn",
										"src":"/static/feed/img/share/twitter-16.png",
									});
									share_btn.click(function(){
										module_share.share_twitter($(this).data("link"),$(this).data("title"));
									});
								d_share.append(share_btn);
								share_btn = $("<img />")
									share_btn.data("link",item.link);
									share_btn.data("title",item.title);
									share_btn.attr({
										"class":"subscription_share_btn",
										"src":"/static/feed/img/share/gplus-16.png",
									});
									share_btn.click(function(){
										module_share.share_gplus($(this).data("link"),$(this).data("title"));
									});
								d_share.append(share_btn);
							td.append(d_share);
						
						tr_detail.append(td);
					subscription_list_item_table.append(tr_detail);
					
					tr_brief.click(function(){
						var row_id = $(this).data("row_id");
						var item_id = $(this).data("item_id");
						console.log(row_id);
						
						var row_data = subscription_instance.row_data_dict[row_id];
						var opening_row_id = subscription_instance.opening_row_id;
						
						row_data.readdone = true;
						
						module_momohafeed.subscription_item_set_readdone(
							subscription_instance.subscription_id,
							item_id,
							true,
							null
						);
						
						var tr_brief;
						var tr_detail;
						
						if ( opening_row_id != null ){
							tr_brief = $("#subscription_list_item_row_"+opening_row_id+"_brief");
							tr_detail = $("#subscription_list_item_row_"+opening_row_id+"_detail");
							tr_brief.css("display","table-row");
							tr_detail.css("display","none");
						}
						
						tr_brief = $("#subscription_list_item_row_"+row_id+"_brief");
						tr_detail = $("#subscription_list_item_row_"+row_id+"_detail");
						tr_brief.css("display","none");
						tr_detail.css("display","table-row");
						
						ui_update_subscription_list_item_row_X_brief(row_id);
						
						subscription_instance.opening_row_id = row_id;
					});
					title.click(function(){
						row_id = $(this).data("row_id");
						
						tr_brief = $("#subscription_list_item_row_"+row_id+"_brief");
						tr_detail = $("#subscription_list_item_row_"+row_id+"_detail");
						tr_brief.css("display","table-row");
						tr_detail.css("display","none");
						
						if ( row_id == subscription_instance.opening_row_id ){
							subscription_instance.opening_row_id = null;
						}
					});
					
					ui_update_subscription_list_item_row_X_brief(i);
				} // for(i=0;i<j.item_detail_list.length;++i)
				utils.cb(done_callback);
			} // function(j)
		);
		
	}
	
	var ui_update_subscription_list_item_row_X_brief = function(row_id){
		var row_data = subscription_instance.row_data_dict[row_id];
		var tr_brief = $("#subscription_list_item_row_"+row_id+"_brief");

		tr_brief.toggleClass("subscription_readdone",row_data.readdone);
	}

	return {
		init: init,
		load: load,
	}
	
})();

$(module_subscription.init);
