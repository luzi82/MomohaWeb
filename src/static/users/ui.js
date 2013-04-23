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
			$('#users_auth_login_btn').click(function(){
				var username = $('#users_auth_login_username').val();
				var password = $('#users_auth_login_password').val();
				$("#users_auth_login_username").prop('disabled', true);
				$("#users_auth_login_password").prop('disabled', true);
				$('#users_auth_login_btn').prop('disabled', true);
				users_auth_login_progress(30);
				users.login(username, password, function(success, reason){
					console.log("success "+success);
					if(!success){
						// TODO
						return;
					}
					users_auth_login_progress(100);
				});
			});
			
			feed_root_layout.body_maintain();
		});
	};
	
	var show_login = function(){
		console.log("show_login");
		$(".app").hide();
		
		$("#users_auth").show();
		$("#users_auth_login_progress").hide();
		$("#users_auth_login_username").prop('disabled', false);
		$("#users_auth_login_password").prop('disabled', false);
		$('#users_auth_login_btn').prop('disabled', false);
		
		$("#users_app").show();
	};
	
	var users_auth_login_progress = function(val){
		$("#users_auth_login_progress").show();
		$("#users_auth_login_progress_bar").css("width",""+val+"%");
	};
	
	init();
	
	return {
		show_login: show_login,
	};
	
});
