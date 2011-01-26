var a = new Array(0);
Array.prototype.unique = function () {
	var r = new Array();
	o:for(var i = 0, n = this.length; i < n; i++) {
		for(var x = 0, y = r.length; x < y; x++) {
			if(r[x]==this[i]) continue o;
		}
		r[r.length] = this[i];
	}
	return r;
};

Array.prototype.diff = function(mew) {
  var old = this;
  var diff = new Array();
  if(!old.length) {
      return diff;
  }
  if(!mew.length) {
      diff.push(777);
      return diff;
  }
  for(var i=0; i< old.length; i++) {
      for (var j=0; j< mew.length; j++) {
          if (old[i] === mew[j]) old[i] = 0;
      }
  }
  for(var i=0; i< old.length; i++) {
      if (old[i] != 0) diff.push(old[i]);
  }
  return diff;
};
