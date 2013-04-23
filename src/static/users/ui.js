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
		
		$("#header_auth_chpwd").on("click",header_auth_chpwd_click);
		$("#header_auth_logout").on("click",header_auth_logout_click);
		
		$('body').on("login_done",login_true);
		$('body').on("start_verify_login_done",login_true);
		$('body').on("logout_done",login_false);
	};
	
	var header_auth_logout_click = function(){
		users.logout();
		login_false();
	};
	
	var header_auth_chpwd_click = function(){
	}
	
	var load_login_ui_done = false;
	var load_login_ui = function(callback){
		if(!load_login_ui_done){
			$("#module_users").load("/static/users/ui.html #users_import",function(){
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
							$("#users_auth_login_progress").hide();
							$("#users_auth_login_username").prop('disabled', false);
							$("#users_auth_login_password").prop('disabled', false);
							$('#users_auth_login_btn').prop('disabled', false);
							return;
						}
						users_auth_login_progress(100);
					});
				});
				$('#users_auth_reg_btn').click(function(){
					var password0 = $('#users_auth_reg_password0').val();
					var password1 = $('#users_auth_reg_password1').val();
					if(password0!=password1){
						return;
					}
					var username = $('#users_auth_reg_username').val();
					var password = password0;
					$("#users_auth_reg_username").prop('disabled', true);
					$("#users_auth_reg_password").prop('disabled', true);
					$('#users_auth_reg_btn').prop('disabled', true);
					users_auth_reg_progress(30);
					users.add_user(username, password, function(success, reason){
						console.log("success "+success);
						if(!success){
							$("#users_auth_reg_progress").hide();
							$("#users_auth_reg_username").prop('disabled', false);
							$("#users_auth_reg_password").prop('disabled', false);
							$('#users_auth_reg_btn').prop('disabled', false);
							return;
						}
						users_auth_reg_progress(100);
					});
				});
				
				feed_root_layout.body_maintain();
				if(callback){callback();}
			});
		}else{
			if(callback){callback();}
		}
	}
	
	var show_login = function(){
		console.log("show_login");
		load_login_ui(function(){
			$(".app").hide();
			
			$("#users_auth").show();

			$("#users_auth_login_progress").hide();
			$("#users_auth_login_username").prop('disabled', false);
			$("#users_auth_login_password").prop('disabled', false);
			$('#users_auth_login_btn').prop('disabled', false);
			
			$("#users_auth_reg_progress").hide();
			$("#users_auth_reg_username").prop('disabled', false);
			$("#users_auth_reg_password").prop('disabled', false);
			$('#users_auth_reg_btn').prop('disabled', false);
			
			$("#users_app").show();
		});
	};
	
	var users_auth_login_progress = function(val){
		$("#users_auth_login_progress").show();
		$("#users_auth_login_progress_bar").css("width",""+val+"%");
	};
	
	var users_auth_reg_progress = function(val){
		$("#users_auth_reg_progress").show();
		$("#users_auth_reg_progress_bar").css("width",""+val+"%");
	};
	
	var login_true = function(){
		$('.auth',"#header").show();
	}
	
	var login_false = function(){
		$('.auth',"#header").hide();
	}
	
	init();
	
	return {
		show_login: show_login,
	};
	
});
