define([
	"jquery",
	"auth",
	"feed_root_layout"
], function(
	$
	, auth
	, feed_root_layout
) {

	var init = function(){
		var import_div = $('<div id="module_auth" />');
		$("#import").append(import_div);
		
		$("#header_auth_chpwd").on("click",header_auth_chpwd_click);
		$("#header_auth_logout").on("click",header_auth_logout_click);
		
		$('body').on("login_done",login_true);
		$('body').on("start_verify_login_done",login_true);
		$('body').on("logout_done",login_false);
	};
	
	var header_auth_logout_click = function(){
		auth.logout();
		login_false();
	};
	
	var header_auth_chpwd_click = function(){
		load_ui(function(){
			$("#auth_chpwd_progress").hide();
			$("#auth_chpwd_old_password_input").prop('disabled', false);
			$("#auth_chpwd_password0_input").prop('disabled', false);
			$("#auth_chpwd_password1_input").prop('disabled', false);
			$('#auth_chpwd_submit_btn').prop('disabled', false);

			$("#auth_chpwd_modal").modal("show");
		});
	}
	
	var load_ui_done = false;
	var load_ui = function(callback){
		if(!load_ui_done){
			$("#module_auth").load("/static/auth/ui.html #auth_import",function(){
				$('#auth_login_btn').click(function(){
					var username = $('#auth_login_username').val();
					var password = $('#auth_login_password').val();
					$("#auth_login_username").prop('disabled', true);
					$("#auth_login_password").prop('disabled', true);
					$('#auth_login_btn').prop('disabled', true);
					auth_login_progress(30);
					auth.login(username, password, function(success, reason){
						console.log("success "+success);
						if(!success){
							$("#auth_login_progress").hide();
							$("#auth_login_username").prop('disabled', false);
							$("#auth_login_password").prop('disabled', false);
							$('#auth_login_btn').prop('disabled', false);
							return;
						}
						auth_login_progress(100);
					});
				});
				
				$('#auth_reg_btn').click(function(){
					var password0 = $('#auth_reg_password0').val();
					var password1 = $('#auth_reg_password1').val();
					if(password0!=password1){
						return;
					}
					var username = $('#auth_reg_username').val();
					var password = password0;
					$("#auth_reg_username").prop('disabled', true);
					$("#auth_reg_password").prop('disabled', true);
					$('#auth_reg_btn').prop('disabled', true);
					auth_reg_progress(30);
					auth.add_user(username, password, function(success, reason){
						console.log("success "+success);
						if(!success){
							$("#auth_reg_progress").hide();
							$("#auth_reg_username").prop('disabled', false);
							$("#auth_reg_password").prop('disabled', false);
							$('#auth_reg_btn').prop('disabled', false);
							return;
						}
						auth_reg_progress(100);
					});
				});
				
				$('#auth_chpwd_submit_btn').click(function(){
					var old_password = $('#auth_chpwd_old_password_input').val();
					var password0 = $('#auth_chpwd_password0_input').val();
					var password1 = $('#auth_chpwd_password1_input').val();
					if(password0!=password1){
						return;
					}
					$("#auth_chpwd_old_password_input").prop('disabled', true);
					$("#auth_chpwd_password0_input").prop('disabled', true);
					$("#auth_chpwd_password1_input").prop('disabled', true);
					$('#auth_chpwd_submit_btn').prop('disabled', true);
					auth_chpwd_progress(30);
					auth.set_password(old_password, password0, function(success, reason){
						console.log("success "+success);
						if(!success){
							$("#auth_chpwd_progress").hide();
							$("#auth_chpwd_old_password_input").prop('disabled', false);
							$("#auth_chpwd_password0_input").prop('disabled', false);
							$("#auth_chpwd_password1_input").prop('disabled', false);
							$('#auth_chpwd_submit_btn').prop('disabled', false);
							return;
						}
						auth_chpwd_progress(100);
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
		load_ui(function(){
			$(".app").hide();
			
			$("#auth").show();

			$("#auth_login_progress").hide();
			$("#auth_login_username").prop('disabled', false);
			$("#auth_login_password").prop('disabled', false);
			$('#auth_login_btn').prop('disabled', false);
			
			$("#auth_reg_progress").hide();
			$("#auth_reg_username").prop('disabled', false);
			$("#auth_reg_password").prop('disabled', false);
			$('#auth_reg_btn').prop('disabled', false);
			
			$("#auth_app").show();
		});
	};
	
	var auth_chpwd_progress = function(val){
		$("#auth_chpwd_progress").show();
		$("#auth_chpwd_progress_bar").css("width",""+val+"%");
	}
	
	var auth_login_progress = function(val){
		$("#auth_login_progress").show();
		$("#auth_login_progress_bar").css("width",""+val+"%");
	};
	
	var auth_reg_progress = function(val){
		$("#auth_reg_progress").show();
		$("#auth_reg_progress_bar").css("width",""+val+"%");
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
