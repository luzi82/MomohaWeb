define([
	"jquery",
	"kyubeyuser",
	"feed_utils",
], function(
	$
	, kyubeyuser
	, feed_utils
) {
	
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
		// register: register,
		verify_login: verify_login,
	};

});
