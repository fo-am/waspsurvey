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

function in_list(v,l) {
    return l.includes(v);
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

function push_slider(v,slider_id) {
    $("#"+slider_id).val(v);
}

function link_slider(from,to) {
    $("#"+to).hide();
    $("#"+from).on("change", function(event) {
	$("#"+to).val(event.target.value);
    });    
}


function link_insect_selector(from,to,filt) {
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

    var container = "#"+from+"-container";
    if (filt!="" && !in_list(from,filt)) {
		$(container).hide();
    }
}

function insect_selector_none(to) {
    $("#"+to).val("none");
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

function link_insect_wasp_bee(from,to,filt) {
    $("#"+to).val("");
    $("#"+to).hide();
    $("#"+from+"-wasp").on("change", function(event) {
	var o = csv_to_object($("#"+to).val());	
	l = object_add(o,from,"wasp")
	$("#"+to).val(object_to_csv(o));
    }); 
    $("#"+from+"-bee").on("change", function(event) {
	var o = csv_to_object($("#"+to).val());	
	l = object_add(o,from,"bee")
	$("#"+to).val(object_to_csv(o));
    }); 
    $("#"+from+"-none").on("change", function(event) {
	var o = csv_to_object($("#"+to).val());	
	l = object_add(o,from,"neither")
	$("#"+to).val(object_to_csv(o));
    });

    // shuffle em up
    var cards = $("[id^="+from+"-holder]");
    for(var i = 0; i < cards.length; i++){
	var target = Math.floor(Math.random() * cards.length -1) + 1;
	var target2 = Math.floor(Math.random() * cards.length -1) +1;
	cards.eq(target).before(cards.eq(target2));
    }

    var container = "#"+from+"-container";
    if (filt!="" && !in_list(from,filt)) {
		$(container).parent().hide();
    }	
}

//////////////////////////////////////////////////////////

var insects = [];
function clear_insects() { insects = []; }
function add_insect(id,image,filt) {
    if (filt=="" || in_list(id,filt)) {
	insects.push([id,image]);
    }
}

function setup_insects_feel(id) {
    var dest = $("#id_"+id);
    var slider = $("#feelslider-"+id);
    var index = 0;

    dest.hide();

    // show first image
    if (insects.length>0) {
	$("#insect_img").attr("src","/"+insects[index][1]);
    }
          
    handler=function (ev) {
	// if we haven't run out of insects yet
	if (index<insects.length-1) {
	    // override form submit event...
	    ev = ev || window.event;
	    if(ev.preventDefault) { 
		ev.preventDefault();    
	    }
	}

	// insert into current object
	var o = csv_to_object(dest.val());	
	l = object_add(o,insects[index][0],slider.val())
	dest.val(object_to_csv(o));

	index++;
	$("#insect_img").attr("src","/"+insects[index][1]);
	// reset slider
	slider.val(50);
    }
    
    form = $("#form_root")[0];
    if (form.addEventListener) form.addEventListener('submit', handler, false);  
    if (form.attachEvent) form.attachEvent('onsubmit', handler);       
}
    
//////////////////////////////////////////////////////////

function link_other_field(id) {
    var w = $("#"+id);
    // find and hide the div box we are in
    w=w.parent().parent();
    w.hide();
    
    // get the previous question's options
    var pw = w.prev();
    var source_id = "id_"+pw[0].id;
    var els = $("[id^="+source_id+"]");
    var index=0;
    
    els.each(function () {
	if (this.type=='checkbox') {
	    // fade in when the last one is selected
	    if (index==els.length-1) {
		this.addEventListener('change',function() {
		    if (this.checked) {
			w.fadeIn(500);
		    } else {
			w.fadeOut(500);
		    }
		});
	    } 
	}

	if (this.type=="radio") {	
	    // fade in when the last one is selected
	    if (index==els.length-1) {
		this.addEventListener('change',function() { w.fadeIn(500); });
	    } else {
		// otherwise fade out again
		this.addEventListener('change',function() { w.fadeOut(500); });
	    }
	}
	
	index++;
    });
}

//////////////////////////////////////////////////////////


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
