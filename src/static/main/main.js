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
		momohafeed: '/feed/cmd',
    },
    shim: {
        'bootstrap': {deps: ['jquery']},
        'cookie': {deps: ['jquery']},
        'json': {deps: ['jquery']},
    }
});

require([
	"jquery",
	"bootstrap",
	"cookie",
	"json",
	"feed_utils",
	"feed_root_layout",
	"feed_add_subscription",
	"feed_list_subscription",
	"feed_subscription",
	"feed_share",
	"momohafeed",
], function(
) {
});
