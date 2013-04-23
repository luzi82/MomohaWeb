requirejs.config({
    baseUrl: '/static',
    paths: {
        jquery: 'jquery/jquery-1.9.1',
        bootstrap: 'bootstrap/js/bootstrap',
        cookie: 'cookie/jquery.cookie',
        json: 'json/json2',

		feed_ui: 'feed/ui',
        feed_utils: 'feed/utils',
		feed_root_layout: 'feed/root_layout',
		feed_add_subscription: 'feed/add_subscription',
		feed_list_subscription: 'feed/list_subscription',
		feed_subscription: 'feed/subscription',
		feed_share: 'feed/share',
		
		users: 'users/users',
		users_ui:	'users/ui',

		momohafeed: '/feed/cmd',
		kyubeyuser: '/users/cmd',
    },
    shim: {
        'bootstrap': {deps: ['jquery']},
        'cookie': {deps: ['jquery']},
        'json': {deps: ['jquery']},
    }
});

require([
	"jquery",
	"users",
	"users_ui",
	"feed_root_layout",
	"feed_ui",
	
	"bootstrap",
	"cookie",
	"json",

	"feed_utils",
	"feed_add_subscription",
	"feed_list_subscription",
	"feed_subscription",
	"feed_share",
	
	"momohafeed",
], function(
	$
	, users
	, users_ui
	, feed_root_layout
	, feed_ui
) {
	console.log("main");
	
	var login_true = function(){
		feed_ui.show();
	};
	
	var login_false = function(){
		feed_ui.hide();
		users_ui.show_login();
	};
	
	$("body").on("login_done",login_true);
	$("body").on("start_verify_login_done",login_true);
	$("body").on("logout_done",login_false);
	$("body").on("start_verify_login_fail",login_false);
	
	users.verify_login(function(success){
		// console.log("verify_login: "+success);
		if(success){
			$("body").trigger("start_verify_login_done");
		}else{
			$("body").trigger("start_verify_login_fail");
		}
	});
});
