var module_subscription = (function(){

	var load = function(subscription_id){
		
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
						td.append(title);
						
						d_content = $("<div />");
						d_content.html(item.content);
						td.append(d_content);
					
					tr_detail.append(td);
				subscription_list_item_table.append(tr_detail);
				
				tr_brief.click(function(){
					row_id = $(this).data("row_id");
					console.log(row_id);
					tr_brief = $("#subscription_list_item_row_"+row_id+"_brief");
					tr_detail = $("#subscription_list_item_row_"+row_id+"_detail");
					tr_brief.css("display","none");
					tr_detail.css("display","table-row");
				});
				tr_detail.click(function(){
					row_id = $(this).data("row_id");
					tr_brief = $("#subscription_list_item_row_"+row_id+"_brief");
					tr_detail = $("#subscription_list_item_row_"+row_id+"_detail");
					tr_brief.css("display","table-row");
					tr_detail.css("display","none");
				});
			}
		});
		
	}

	return {
		load: load
	}
	
})();
