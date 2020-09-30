function link_slider(from,to) {
    $("#"+to).hide();
    $("#"+from).on("change", function(event) {
	console.log(event.target.value);
	$("#"+to).val(event.target.value);
    });    
}

function link_insect_selector(from,to) {
    $("#"+from).on("change", function(event) {
	console.log(event.target.value);
	console.log(to);
	$("#"+to).val(event.target.value);
    }); 
}
