define([
	"jquery",
	"users",
	"feed_root_layout"
], function(
	$
	, users
	, feed_root_layout
) {

	var init = function(){
		var import_div = $('<div id="module_users" />');
		$("#import").append(import_div);
		import_div=$("#module_users");
		
		import_div.load("/static/users/ui.html #users_import",function(){
			feed_root_layout.body_maintain();
		});
	};
	
	var show_login = function(){
		console.log("show_login");
		$(".app").hide();
		$("#users_auth").show();
		$("#users_app").show();
	};
	
	init();
	
	return {
		show_login: show_login,
	};
	
});
