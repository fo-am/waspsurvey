function link_slider(from,to) {
    $("#"+to).hide();
    $("#"+from).on("change", function(event) {
	console.log(event.target.value);
	$("#"+to).val(event.target.value);
    });    
}
