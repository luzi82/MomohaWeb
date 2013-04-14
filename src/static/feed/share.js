var module_share = (function(){

	var share_facebook = function(link,title){
		var shareurl = "http://www.facebook.com/sharer/sharer.php?u=" + encodeURI(link);
	 	window.open(shareurl,'','width=550,height=350,menubar=no,status=no');
	}

	var share_twitter = function(link,title){
		var shareurl = "http://twitter.com/share?url=" + encodeURI(link) + "&text=" + encodeURI(title);
		window.open(shareurl,'','width=550,height=300,menubar=no,status=no');
	}

	var share_gplus = function(link,title){
		var shareurl = "https://plus.google.com/share?url=" + encodeURI(link);
	 	window.open(shareurl,'','width=600,height=600,menubar=no,status=no');
	}
	
	var share_btn_click = function(){
		var link = $(this).data("link");
		var title = $(this).data("title");
		if($(this).hasClass("share_facebook")){
			share_facebook(link,title);
		}else if($(this).hasClass("share_twitter")){
			share_twitter(link,title);
		}else if($(this).hasClass("share_gplus")){
			share_gplus(link,title);
		}
	}
	
	return {
		share_btn_click : share_btn_click ,
	}
	
})();
