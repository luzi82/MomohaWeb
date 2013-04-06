var module_subscription = (function(){
	
	var subscription_instance = null;

	var load = function(subscription_id){
		
		subscription_instance = {
			subscription_id: subscription_id,
			opening_row_id: null,
		};
		
		subscription_list_item_table = $("#subscription_list_item_table");
		subscription_list_item_table.empty();
		
		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/feed/j_subscription_list_item_detail/",
			data: {
				csrfmiddlewaretoken: $.cookie('csrftoken'),
				subscription_id: subscription_id,
			},
		}).done(function(j){
			console.log(JSON.stringify(j));
			for(i=0;i<j.item_detail_list.length;++i){
				item = j.item_detail_list[i];
				
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
						td.append(d_content);
					
					tr_detail.append(td);
				subscription_list_item_table.append(tr_detail);
				
				tr_brief.click(function(){
					row_id = $(this).data("row_id");
					item_id = $(this).data("item_id");
					console.log(row_id);
					
					opening_row_id = subscription_instance.opening_row_id;
					
					$.ajax({
						type: "POST",
						dataType: "json",
						url: "/feed/j_subscription_item_set_readdone/",
						data: {
							csrfmiddlewaretoken: $.cookie('csrftoken'),
							subscription_id: subscription_instance.subscription_id,
							item_id: item_id,
							value: true,
						},
					});
					
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
			}
		});
		
	}

	return {
		load: load
	}
	
})();
