define([
	"jquery",
	"momohafeed",
	"feed_share",
	"feed_utils",
], function(
	$
	, momohafeed
	, feed_share
	, feed_utils
) {
	
	var PHI = (1.0+Math.sqrt(5.0))/2.0;
	
	var LOAD_ITEM_COUNT = 64;

	var subscription_instance = null;
	
	var show_all = false;
	
	var init = function(){
		
		$("#subscription_poll_btn").click(function(){
			if(subscription_instance==null)
				return;
			$("#subscription_list_item_table").empty();
			load_bar(10);
			momohafeed.subscription_poll(
				subscription_instance.subscription_id,
				function(j){
					load(subscription_instance.subscription_id,null);
				},
				null // TODO issue 97
			);
		});

		$("#subscription_all_readdone_btn").click(function(){
			if(subscription_instance==null)
				return;
			load_bar(10);
			momohafeed.subscription_all_readdone(
				subscription_instance.subscription_id,
				function(j){
					load(subscription_instance.subscription_id,null);
				},
				null // TODO issue 98
			);
		});
		
		$("#subscription_filter_showall_btn").click(function(){
			if(subscription_instance==null)
				return;
			$("#subscription_list_item_table").empty();
			show_all = true;
			ui_update_subscription_filter_btn();
			load(subscription_instance.subscription_id,null);
		});

		$("#subscription_filter_shownew_btn").click(function(){
			if(subscription_instance==null)
				return;
			$("#subscription_list_item_table").empty();
			show_all = false;
			ui_update_subscription_filter_btn();
			load(subscription_instance.subscription_id,null);
		});

		$("#subscription_show_rm_modal_btn").click(subscription_show_rm_modal_btn_click);
		
		$("#subscription_show_rename_modal_btn").click(subscription_show_rename_modal_btn_click);

		$("#subscription_main").scroll(subscription_main_scroll);

		$("#import").append($('<div id="module_subscription" />'));
		$("#module_subscription").load("inc/feed/subscription.html #subscription_import",function(){
			$("#subscription_rm_modal_submit_btn").click(subscription_rm_modal_submit_btn_click);
			$("#subscription_rename_modal_submit_btn").click(subscription_rename_modal_submit_btn_click);
		});

		ui_update_subscription_filter_btn();
	}

	var load = function(subscription_id,done_callback){
		
		$("#subscription_area").show();
		
		subscription_instance = {
			// instance const
			subscription_id: subscription_id,
			
			// data			
			vm_subscription_detail: null,
			row_data_dict: {},
			row_data_next: 0,
			
			// load
			range_published: null,
			range_id: null,
			load_end: false,
			load_busy: false,
			
			// open/close
			opening_row_id: null,
		};

		$("#subscription_main_title").hide();
		$("#subscription_list_item_table").empty();
		load_bar(90);
		
		var subscription_header = $("#subscription_header_template").clone();
			subscription_header.attr("id","subscription_header");
		$("#subscription_list_item_table").append(subscription_header);
		
		momohafeed.subscription_detail(
			subscription_id,
			function(j){
				var vm_subscription_detail = j.subscription_detail;
				subscription_instance.vm_subscription_detail = vm_subscription_detail;
				
				var subscription_header = $("#subscription_header");
				
				$(".title_text",subscription_header).text(vm_subscription_detail.title);
				$(".last_poll_text",subscription_header).text(vm_subscription_detail.last_poll_txt);
				$(".link").attr({
					"href": vm_subscription_detail.link,
					"target": "_blank",
				});
				subscription_header.show();
			},
			null // TODO issue 99
		);

		load_bar(100);
		
		load_more_enough(null, null, null); // TODO issue 100
		
		feed_utils.cb(done_callback);
	};
	
	var load_more = function(done_callback,fail_callback){
		
		if(subscription_instance.load_end){
			feed_utils.cb(done_callback);
			return;
		}
		
		momohafeed.subscription_list_item_detail(
			subscription_instance.subscription_id,
			show_all,
			subscription_instance.range_published,
			subscription_instance.range_id,
			LOAD_ITEM_COUNT,
			function(j){
				console.log(JSON.stringify(j));
				if(j.item_detail_list.length<LOAD_ITEM_COUNT){
					subscription_instance.load_end = true;
				}else{
					subscription_instance.range_published = j.item_detail_list[LOAD_ITEM_COUNT-1].published;
					subscription_instance.range_id = j.item_detail_list[LOAD_ITEM_COUNT-1].id;
				}
				for(var i=0;i<j.item_detail_list.length;++i){
					var item = j.item_detail_list[i];
					
					var row_data = {
						vm_item: item,
						readdone: (item["readdone"]!=0),
						star: (item["star"]!=0),
					};
					
					var row_id = subscription_instance.row_data_next++;
					subscription_instance.row_data_dict[row_id] = row_data;
					
					var brief_body = $("#subscription_item_brief_template").clone();
						brief_body.attr("id","subscription_item_brief_"+row_id);
						brief_body.data("row_id",row_id);
						fill_subscription_item(brief_body,item);
					$("#subscription_list_item_table").append(brief_body);
					
					var detail_body = $("#subscription_item_detail_template").clone();
						detail_body.attr("id","subscription_item_detail_"+row_id);
						detail_body.data("row_id",row_id);
						detail_body.data("fill_done",false);
						// fill_subscription_item(detail_body,item);
					$("#subscription_list_item_table").append(detail_body);
					
					ui_update_subscription_item(row_id);
					brief_body.show();
					
				} // for(i=0;i<j.item_detail_list.length;++i)
				// $(".subscription_item_brief").show();
				
				feed_utils.cb(done_callback);
				
			} , // function(j)
			fail_callback
		);
		
	};
	
	var load_more_enough = function(done_callback,busy_callback,fail_callback){
		if(subscription_instance.load_busy){
			feed_utils.cb(busy_callback);
			return;
		}
		subscription_instance.load_busy = true;
		var dcb = done_callback;
		var fcb = fail_callback;
		load_more_enough_loop(
			function(){
				subscription_instance.load_busy = false;
				feed_utils.cb(dcb);
			},
			function(){
				subscription_instance.load_busy = false;
				feed_utils.cb(fcb);
			}
		);
	};
	
	var load_more_enough_loop = function(done_callback,fail_callback){
		var dcb = done_callback;
		var fcb = fail_callback;
		// console.log($("#subscription_main").height());
		// console.log($("#subscription_main").scrollTop());
		// console.log($("#subscription_list_item_table").height());
		if(subscription_instance.load_end){
			feed_utils.cb(done_callback);
			return;
		}
		if(
			(
				$("#subscription_list_item_table").height()
				-$("#subscription_main").scrollTop()
				-$("#subscription_main").height()
			)
			/ ( ($("#subscription_main").height()) * 1.0 ) > (PHI*PHI)
		){
			feed_utils.cb(done_callback);
			return;
		}
		load_more(
			function(){
				load_more_enough_loop(dcb,fcb);
			},
			fail_callback
		);
	};
	
	var ui_update_subscription_item = function(row_id){
		var row_data = subscription_instance.row_data_dict[row_id];
		var subscription_item_brief  = $("#subscription_item_brief_" +row_id);
		var subscription_item_detail = $("#subscription_item_detail_"+row_id);
		
		subscription_item_brief.toggleClass("subscription_readdone",row_data.readdone);
		$(".subscription_star",subscription_item_brief ).toggleClass("icon-star-empty", !row_data.star);
		$(".subscription_star",subscription_item_brief ).toggleClass("icon-star"      , row_data.star);
		$(".subscription_star",subscription_item_detail).toggleClass("icon-star-empty", !row_data.star);
		$(".subscription_star",subscription_item_detail).toggleClass("icon-star"      , row_data.star);
	}
	
	var ui_update_subscription_filter_btn = function(){
		if(show_all){
			$("#subscription_filter_btn_icon").attr("class","icon-list-alt");
			$("#subscription_filter_btn_txt").text("Show ALL");
		}else{
			$("#subscription_filter_btn_icon").attr("class","icon-asterisk");
			$("#subscription_filter_btn_txt").text("Show NEW");
		}
	}
	
	var load_bar = function(percent){
		if(percent<100){
			$("#subscription_progress_bar").css("width",percent+"%");
			$("#subscription_progress").show();
		}else{
			$("#subscription_progress").hide();
		}
	}
	
	var subscription_show_rm_modal_btn_click = function(e){
		if(subscription_instance==null){
			e.preventDefault();
			return;
		}
		$("#subscription_rm_modal_progress").hide();
	}

	var subscription_show_rename_modal_btn_click = function(e){
		if(subscription_instance==null){
			e.preventDefault();
			return;
		}
		$("#subscription_rename_modal_progress").hide();
	}
	
	var subscription_rm_modal_submit_btn_click = function(){
		if(subscription_instance==null)
			return;
		
		$("#subscription_rm_modal_progress_bar").css("width","10%");
		$("#subscription_rm_modal_progress").show();
		
		momohafeed.subscription_set_enable(
			subscription_instance.subscription_id,
			false,
			function(){
				// TODO: issue 73:
				// subscription_rm_modal_submit_btn_click: should call rm-listener instead of calling outer module
				require([
					"feed_list_subscription",
					"feed_root_layout",
				], function(
					feed_list_subscription ,
					feed_root_layout
				){
					$("#subscription_rm_modal_progress_bar").css("width","90%");
					feed_list_subscription.refresh(function(){
						feed_root_layout.hide_mainarea();
						$("#subscription_rm_modal").modal("hide");
					});
				});
			},
			null // TODO issue 101
		);
	}
	
	var subscription_rename_modal_submit_btn_click = function(){
		if(subscription_instance==null)
			return;

		var newName = $("#subscription_rename_name_input").val();
		if(newName==""){
			newName = null;
		}
		
		$("#subscription_rename_modal_progress_bar").css("width","10%");
		$("#subscription_rename_modal_progress").show();
		
		momohafeed.subscription_set_title(
			subscription_instance.subscription_id,
			newName,
			function(){
				// FIXME should call external rename listener
				require([
					"feed_list_subscription",
					"feed_root_layout",
				], function(
					feed_list_subscription ,
					feed_root_layout
				){
					$("#subscription_rename_modal_progress_bar").css("width","90%");
					feed_list_subscription.refresh(null);
					load(subscription_instance.subscription_id,null);
					$("#subscription_rename_modal").modal("hide");
				});
			},
			null // FIXME
		);
	}
	
	var fill_subscription_item = function(subscription_item,item) {
		var row_id = subscription_item.data("row_id");
		var row_data = subscription_instance.row_data_dict[row_id];
		
		$(".title_text",subscription_item).text(item.title);
		$(".published_text",subscription_item).text(item.published_txt);
		$(".link",subscription_item).attr({
			"href" : item.link,
			"target" : "_blank",
		});
		$(".content",subscription_item).html(item.content);
		
		$(".click_open_detail",subscription_item).data("row_id", row_id);
		$(".click_open_detail",subscription_item).click(click_open_detail);
		$(".click_close_detail",subscription_item).data("row_id", row_id);
		$(".click_close_detail",subscription_item).click(click_close_detail);
		$(".subscription_share_btn",subscription_item).data("link",item.link);
		$(".subscription_share_btn",subscription_item).data("title",item.title);
		$(".subscription_share_btn",subscription_item).click(feed_share.share_btn_click);
		$(".stop_propagation",subscription_item).click(stop_propagation);
		$(".subscription_star",subscription_item).data("row_id", row_id);
		$(".subscription_star",subscription_item).click(subscription_star_click);
	}
	
	var click_open_detail = function(){
		var row_id = $(this).data("row_id");
		var row_data = subscription_instance.row_data_dict[row_id];
		
		if(subscription_instance.opening_row_id!=null){
			$("#subscription_item_brief_"+subscription_instance.opening_row_id).show();
			$("#subscription_item_detail_"+subscription_instance.opening_row_id).hide();
		}
		
		if(!($("#subscription_item_detail_"+row_id).data("fill_done"))){
			fill_subscription_item($("#subscription_item_detail_"+row_id), row_data.vm_item);
			$("#subscription_item_detail_"+row_id).data("fill_done",true);
		}
		
		$("#subscription_item_brief_"+row_id).hide();
		$("#subscription_item_detail_"+row_id).show();
		subscription_instance.opening_row_id = row_id;

		row_data.readdone = true;
		momohafeed.subscription_item_set_readdone(
			subscription_instance.subscription_id,
			row_data.vm_item.id,
			true,
			null, // no callback
			null // TODO issue 102
		);
		ui_update_subscription_item(row_id);
	}
	
	var click_close_detail = function(){
		var row_id = $(this).data("row_id");
		$("#subscription_item_brief_"+row_id).show();
		$("#subscription_item_detail_"+row_id).hide();
		subscription_instance.opening_row_id = null;
	}
	
	var stop_propagation = function(e){
		e.stopPropagation();
	}
	
	var subscription_star_click = function(){
		var row_id = $(this).data("row_id");
		var row_data = subscription_instance.row_data_dict[row_id];
		
		row_data.star = !row_data.star;
		
		momohafeed.subscription_item_set_star(
			subscription_instance.subscription_id,
			row_data.vm_item.id,
			row_data.star,
			null, // no callback
			null // TODO issue 103
		);
		
		ui_update_subscription_item(row_id);
	};
	
	var subscription_main_scroll = function(){
		if(
			(
				$("#subscription_list_item_table").height()
				-$("#subscription_main").scrollTop()
				-$("#subscription_main").height()
			)
			/ ( ($("#subscription_main").height()) * 1.0 ) < (PHI)
		){
			load_more_enough(null,null,null); // FIXME
			return;
		}
	};
	
	init();
	
	return {
		load: load,
	}
	
});
