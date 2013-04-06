var utils = (function(){
	
	var cb = function(callback){
		if(callback!=null){
			callback();
		}
	}
	
	return {
		cb: cb
	};
	
})();
