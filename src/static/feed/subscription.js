var module_subscription = (function(){
	
	var subscription_area;
	var subscription_progress_bar;
	var subscription_progress;
	var subscription_list_item_table
	var subscription_show_rm_modal_btn;
	
	var subscription_instance = null;
	
	var show_all = false;
	
	var init = function(){
		
		subscription_area = $("#subscription_area");
		subscription_progress = $("#subscription_progress");
		subscription_progress_bar = $("#subscription_progress_bar");
		subscription_list_item_table = $("#subscription_list_item_table");
		subscription_show_rm_modal_btn = $("subscription_show_rm_modal_btn");
		
		var subscription_poll_btn = $("#subscription_poll_btn");
		subscription_poll_btn.click(function(){
			if(subscription_instance==null)
				return;
			subscription_list_item_table.empty();
			load_bar(10);
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
			load_bar(10);
			module_momohafeed.subscription_all_readdone(
				subscription_instance.subscription_id,
				function(j){
					load(subscription_instance.subscription_id,null);
				}
			);
		});
		
		var subscription_filter_showall_btn = $("#subscription_filter_showall_btn");
		subscription_filter_showall_btn.click(function(){
			if(subscription_instance==null)
				return;
			subscription_list_item_table.empty();
			show_all = true;
			ui_update_subscription_filter_btn();
			load(subscription_instance.subscription_id,null);
		});

		var subscription_filter_shownew_btn = $("#subscription_filter_shownew_btn");
		subscription_filter_shownew_btn.click(function(){
			if(subscription_instance==null)
				return;
			subscription_list_item_table.empty();
			show_all = false;
			ui_update_subscription_filter_btn();
			load(subscription_instance.subscription_id,null);
		});

		var import_div = $('<div id="module_subscription" />');
		$("#import").append(import_div);
		import_div=$("#module_subscription");
		
		$("#subscription_show_rm_modal_btn").click(subscription_show_rm_modal_btn_click);

		import_div.load("/static/feed/subscription.html #subscription_import",function(){
			$("#subscription_rm_modal_submit_btn").click(subscription_rm_modal_submit_btn_click);
		});

		ui_update_subscription_filter_btn();
	}

	var load = function(subscription_id,done_callback){
		
		subscription_area.show();
		
		subscription_instance = {
			subscription_id: subscription_id,
			opening_row_id: null,
			vm_item_detail_list: null,
			row_data_dict: {},
		};
		
		subscription_list_item_table.empty();
		
		load_bar(90);
		
		module_momohafeed.subscription_list_item_detail(
			subscription_id,
			show_all,
			function(j){
				console.log(JSON.stringify(j));
				subscription_instance.vm_item_detail_list = j.item_detail_list;
				for(var i=0;i<j.item_detail_list.length;++i){
					var item = j.item_detail_list[i];
					
					var row_data = {
						vm_item: item,
						readdone: (item["readdone"]!=0),
						tr_brief: null,
						tr_detail: null,
					};
					subscription_instance.row_data_dict[i] = row_data;
					
					var td;
					
					var tr_brief = $('<tr />'); row_data.tr_brief = tr_brief;
						// tr_brief.attr("id","subscription_list_item_row_"+i+"_brief");
						tr_brief.data("row_id",i);
						// tr_brief.data("item_id",item.id);
						tr_brief.css("cursor","pointer");
						td = $('<td />');
						
							td.text(item.title);
						
						tr_brief.append(td);
					subscription_list_item_table.append(tr_brief);
					
					var tr_detail = $('<tr />'); row_data.tr_detail = tr_detail;
						// tr_detail.attr("id","subscription_list_item_row_"+i+"_detail");
						tr_detail.data("row_id",i);
						tr_detail.css("display","none");
						td = $('<td />');
						
							var detail_title = $("<h4 />");
								detail_title.text(item.title);
								detail_title.css("cursor","pointer");
								detail_title.data("row_id",i);
							td.append(detail_title);
							
							var detail_content = $("<div />");
								detail_content.html(item.content);
								detail_content.css("margin-bottom","10px");
							td.append(detail_content);
							
							var detail_share = $("<div />");
								var share_btn;
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
								detail_share.append(share_btn);
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
								detail_share.append(share_btn);
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
								detail_share.append(share_btn);
							td.append(detail_share);
						
						tr_detail.append(td);
					subscription_list_item_table.append(tr_detail);
					
					tr_brief.click(function(){
						var row_id = $(this).data("row_id");
						var row_data = subscription_instance.row_data_dict[row_id];
						
						var opening_row_id = subscription_instance.opening_row_id;
						
						row_data.readdone = true;
						
						module_momohafeed.subscription_item_set_readdone(
							subscription_instance.subscription_id,
							row_data.vm_item.id,
							true,
							null
						);
						
						var tr_brief;
						var tr_detail;
						
						if ( opening_row_id != null ){
							var opening_row_data = subscription_instance.row_data_dict[opening_row_id];
							opening_row_data.tr_brief.css("display","table-row");
							opening_row_data.tr_detail.css("display","none");
						}
						
						row_data.tr_brief.css("display","none");
						row_data.tr_detail.css("display","table-row");
						
						ui_update_subscription_list_item_row_X_brief(row_id);
						
						subscription_instance.opening_row_id = row_id;
					});
					detail_title.click(function(){
						var row_id = $(this).data("row_id");
						var row_data = subscription_instance.row_data_dict[row_id];
						
						row_data.tr_brief.css("display","table-row");
						row_data.tr_detail.css("display","none");
						
						if ( row_id == subscription_instance.opening_row_id ){
							subscription_instance.opening_row_id = null;
						}
					});
					
					ui_update_subscription_list_item_row_X_brief(i);
				} // for(i=0;i<j.item_detail_list.length;++i)
				load_bar(100);
				utils.cb(done_callback);
			} // function(j)
		);
		
	}
	
	var ui_update_subscription_list_item_row_X_brief = function(row_id){
		var row_data = subscription_instance.row_data_dict[row_id];

		row_data.tr_brief.toggleClass("subscription_readdone",row_data.readdone);
	}
	
	var ui_update_subscription_filter_btn = function(){
		var subscription_filter_btn_icon = $("#subscription_filter_btn_icon");
		var subscription_filter_btn_txt = $("#subscription_filter_btn_txt");
		if(show_all){
			subscription_filter_btn_icon.attr("class","icon-list-alt");
			subscription_filter_btn_txt.text("Show ALL");
		}else{
			subscription_filter_btn_icon.attr("class","icon-filter");
			subscription_filter_btn_txt.text("Show NEW");
		}
	}
	
	var load_bar = function(percent){
		if(percent<100){
			subscription_progress_bar.css("width",percent+"%");
			subscription_progress.show();
		}else{
			subscription_progress.hide();
		}
	}
	
	var subscription_show_rm_modal_btn_click = function(e){
		if(subscription_instance==null){
			e.preventDefault();
			return;
		}
		$("#subscription_rm_modal_progress").hide();
	}
	
	var subscription_rm_modal_submit_btn_click = function(){
		if(subscription_instance==null)
			return;
		
		$("#subscription_rm_modal_progress_bar").css("width","10%");
		$("#subscription_rm_modal_progress").show();
		
		module_momohafeed.subscription_set_enable(
			subscription_instance.subscription_id,
			false,
			function(){
				$("#subscription_rm_modal_progress_bar").css("width","90%");
				module_list_subscription.refresh(function(){
					root_layout.hide_mainarea();
					$("#subscription_rm_modal").modal("hide");
				});
			}
		);
	}
	
	return {
		init: init,
		load: load,
	}
	
})();

$(module_subscription.init);
