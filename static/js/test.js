	function getElementsByClassName(className,ele,tagName){
		var a = [];
		var eles = null;
		if(ele) {
			if(tagName) {
				eles = ele.getElementsByTagName(tagName)
			}
			else {
				eles = ele.getElementsByTagName('*')
			}
		}
		else {
			eles = document.getElementsByTagName('*');
		}
		for(var i = 0; i < eles.length; i ++){
			if(eles[i].className.search(new RegExp("\\b" + className + "\\b")) != -1){
				a.push(eles.item(i));
			}
		}
		return a
	}
    function tttt() {
        var a = getElementsByClassName("list-item");
        var i = 0;
        var c = [];
		var d = [];
		var sum = 0;
		var avg = 0;
        for (i = 0; i < a.length; i ++) {
			var b = getElementsByClassName("price", a[i], "li");
			var j = 0;
			if (b.length > 0) {
				d.push(a[i]);
			}
			for (j = 0; j < b.length; j ++) {
				c.push(b[j]);
			}
        }
		for (i = 0; i < c.length; i ++) {
			var p = c[i].getElementsByTagName("em");
			sum += parseFloat(p[0].innerHTML);
		}
		avg = sum / c.length;
		alert(avg);
		for (i = 0; i < c.length; i ++) {
			var p = c[i].getElementsByTagName("em");
			if (parseFloat(p[0].innerHTML) < avg) {
				d[i].style.border = "1px solid red"; 
			}
		}
    }
