////////////////////////////////////////////////////////////////

function list_to_csv(l) {
    return l.join(",");
}

function csv_to_list(s) {
    if (s=="") return [];
    return s.split(",");
}

function list_contains(l,v) {
    for (var i=0; i<l.length; i++) {
	if (l[i]==v) return true;
    }
    return false;
}


function list_remove(l,v) {
    ret=[];
    for (var i=0; i<l.length; i++) {
	if (l[i]!=v) ret.push(l[i]);
    }
    return ret;
}

function list_add(l,v) {
    if (v!="" && !list_contains(l,v)) {
	l.push(v);
    }
    return l;
}

//////////////////////////////////////////////////////////

function object_to_csv(o) {
    l=[]
    for (var key in o) {
	l.push(key+":"+o[key]);
    }		
    return l.join(",");
}

function csv_to_object(s) {
    if (s=="") return {};
    o = {};
    l = s.split(",");
    for (var i=0; i<l.length; i++) {
	console.log(l[i]);
	kv=l[i].split(":");
	o[kv[0]]=kv[1];
    }
    return o;
}

function object_add(o,k,v) {
    o[k]=v;
}

function object_remove(o,k) {
    delete o[k];
}


/////////////////////////////////////////////////////

function link_slider(from,to) {
    console.log(to);
    $("#"+to).hide();
    $("#"+from).on("change", function(event) {
	console.log(event.target.value);
	$("#"+to).val(event.target.value);
    });    
}


function link_insect_selector(from,to) {
    console.log(to);
    $("#"+to).val("");
    $("#"+to).hide();
    $("#"+from).on("change", function(event) {
	var l = csv_to_list($("#"+to).val());

	if (event.target.checked) {
	    l = list_add(l,event.target.value)
	} else {
	    l = list_remove(l,event.target.value)
	}
	
	$("#"+to).val(list_to_csv(l));
    }); 
}

function link_insect_name(from,to) {
    $("#"+to).val("");
    $("#"+to).hide();
    $("#"+from).on("change", function(event) {
	var o = csv_to_object($("#"+to).val());
	
	l = object_add(o,from,event.target.value)

	$("#"+to).val(object_to_csv(o));
    }); 
}

function update_wasp_id(wasp_id,dest) {
    $("#"+dest).hide();
    $("#"+dest).val(wasp_id);
}


function test() {
    l = ["1","2","3"]
    console.log([1,list_to_csv(l)=="1,2,3"]);
    console.log([2,csv_to_list("1,2,3")[1]==2]);    
    console.log([3,list_contains(l,"2")]);
    console.log([4,list_remove(l,"1").length==2]);    
    console.log(list_add(l,"4"));
    console.log(object_to_csv({one: "3", id: "seven"}));
    console.log(csv_to_object("one:3,id:seven"));
}

//test();
