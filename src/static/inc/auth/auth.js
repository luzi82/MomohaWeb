define([
	"jquery",
	"kyubeyauth",
	"feed_utils",
], function(
	$
	, kyubeyauth
	, feed_utils
) {
	
	var AJAX_ERR = "AJAX_ERR";
	
	var add_user = function(username, password, callback){
		kyubeyauth.add_user(
			username, password,
			function(j){
				if(j.success){
					$("body").trigger("login_done");
				}
				if(callback){
					var reason = j.success?null:(j.reason);
					callback(j.success, reason);
				}
			},
			function(){
				callback(false, AJAX_ERR);
			}
		);
	};
	
	var login = function(username, password, callback){
		kyubeyauth.login(
			username, password,
			function(j){
				if(j.success){
					$("body").trigger("login_done");
				}
				if(callback){
					var reason = j.success?null:(j.reason);
					callback(j.success, reason);
				}
			},
			function(){
				callback(false, AJAX_ERR);
			}
		);
	};
	
	var logout = function(callback){
		kyubeyauth.logout(
			function(j){
				$("body").trigger("logout_done");
				if(callback){callback();}
			},
			null // issue 105
		);
	};

	var set_password = function(old_password, new_password, callback){
		kyubeyauth.user_set_password(
			old_password, new_password,
			function(j){
				if(callback){
					var reason = j.success?null:(j.reason);
					callback(j.success, reason);
				}
			},
			function(){
				callback(false, AJAX_ERR);
			}
		);
	};
	
	var verify_login = function(callback){
		kyubeyauth.verify_login(
			function(j){
				if(callback){
					callback(j.success);
				}
			},
			function(){
				callback(false);
			}
		);
	};
	
	return {
		login: login,
		logout: logout,
		add_user: add_user,
		set_password: set_password,
		verify_login: verify_login,
	};

});
