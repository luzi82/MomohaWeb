define([
	"jquery"
], function(
	$
) {

	var cb = function(callback){
		if(callback!=null){
			callback();
		}
	}
	
	var remote = function(cmd,argv,callback){
		if(argv==null)argv={};
		if(callback==null)callback=function(){};
		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/feed/json/",
			data: {
				csrfmiddlewaretoken: $.cookie('csrftoken'),
				json: JSON.stringify({
					cmd: cmd,
					argv: argv,
				}),
			},
		}).done(callback);
	}
		
	return {
		cb: cb,
		remote: remote,
	};

});
