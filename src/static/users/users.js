define([
	"jquery",
	"kyubeyuser",
	"feed_utils",
], function(
	$
	, kyubeyuser
	, feed_utils
) {
	
	var add_user = function(username, password, callback){
		kyubeyuser.add_user(
			username, password,
			function(j){
				if(j.success){
					$("body").trigger("login_done");
				}
				if(callback){
					var reason = j.success?null:(j.reason);
					callback(j.success, reason);
				}
			}
		);
	};
	
	var login = function(username, password, callback){
		kyubeyuser.login(
			username, password,
			function(j){
				if(j.success){
					$("body").trigger("login_done");
				}
				if(callback){
					var reason = j.success?null:(j.reason);
					callback(j.success, reason);
				}
			}
		);
	};
	
	var logout = function(callback){
		kyubeyuser.logout(
			function(j){
				$("body").trigger("logout_done");
				if(callback){callback();}
			}
		);
	};

	var set_password = function(old_password, new_password, callback){
		kyubeyuser.user_set_password(
			old_password, new_password,
			function(j){
				if(callback){
					var reason = j.success?null:(j.reason);
					callback(j.success, reason);
				}
			}
		);
	};
	
	var verify_login = function(callback){
		kyubeyuser.verify_login(
			function(j){
				if(callback){
					callback(j.success);
				}
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
