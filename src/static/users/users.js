define([
	"jquery",
	"users_ui",
	"kyubeyuser",
	"feed_utils",
], function(
	$
	, users_ui
	, kyubeyuser
	, feed_utils
) {
	
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
		verify_login: verify_login,
	};

});
