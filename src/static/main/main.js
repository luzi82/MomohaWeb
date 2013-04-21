requirejs.config({
    baseUrl: '/static',
    paths: {
        jquery: 'jquery/jquery-1.9.1',
        bootstrap: 'bootstrap/js/bootstrap',
        cookie: 'cookie/jquery.cookie',
        json: 'json/json2',

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
) {
	console.log("main");
	
	var show_login = function(){
		users_ui.show_login();
	};
	
	var login_done = function(){
		
	};
	
	users.verify_login(function(success){
		console.log("verify_login: "+success);
		if(success){
			login_done();
		}else{
			show_login();
		}
	});
});
