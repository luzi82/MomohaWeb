var module_share = (function(){

	var share_facebook = function(link,title){
		shareurl = "http://www.facebook.com/sharer/sharer.php?u=" + encodeURI(link);
	 	window.open(shareurl,'','width=550,height=350,menubar=no,status=no');
	}

	var share_twitter = function(link,title){
		shareurl = "http://twitter.com/share?url=" + encodeURI(link) + "&text=" + encodeURI(title);
		window.open(shareurl,'','width=550,height=300,menubar=no,status=no');
	}

	var share_gplus = function(link,title){
		shareurl = "https://plus.google.com/share?url=" + encodeURI(link);
	 	window.open(shareurl,'','width=600,height=600,menubar=no,status=no');
	}

	return {
		share_facebook: share_facebook,
		share_twitter:  share_twitter,
		share_gplus:	share_gplus,
	}
	
})();
