$(document).ready(function(){
	var counter = 0;

	var isactive = $("#human");

	$('#myCanvas').on("annotate-image-added", function(event, id, path){
		$(".my-image-selector").append("<label id=\"" + id + "\"><input type=\"radio\" name=\"image-selector\" class=\"annotate-image-select\" value=\"" + path + "\" checked id=\"" + id + "\"><img src=\"" + path + "\" width=\"35\" height=\"35\"></label>");
	});
	$('#myCanvas').on("annotate-image-remove", function(event, id, path){
		$(".my-image-selector").remove('label#feedback');
	});
	var options = {
		width: "640",          // Width of canvas
  		height: "400",         // Height of canvas
		color: 'red',
		bootstrap: true,
		images: ['ftp://128.46.75.58/WD1/2016%20Olympics/01_August_Mon/161_2016-08-01_15-27-17-440411.png'],
		onExport: function(image){
			if ($("#exported-image").length > 0){
				$("#exported-image").remove();
			}
			$("body").append("<img src=\"" + image + "\" id=\"exported-image\">");
		},
		selectEvent: "change", // listened event on .annotate-image-select selector to select active images
  		unselectTool: true,   // Add a unselect tool button in toolbar (useful in mobile to enable zoom/scroll)
	}


	$('#myCanvas').annotate(options);

	$(".push-new-image").click(function(event) {
		if (counter === 0){
			$('#myCanvas').annotate("push", "https://www.smashingmagazine.com/wp-content/uploads/2015/06/10-dithering-opt.jpg");
			counter += 1;
		}else{
			$('#myCanvas').annotate("push", {id:"unique_identifier", path:"http://i.imgur.com/RRUe0Mo.png"});
			
		}
	});

	$(".submit-all-images").click(function(event) {
		$('#myCanvas').annotate("getall", null, function(d) {
			console.log(d);
		});
	});

	$(".submit-image").click(function(event) {
		$('#myCanvas').annotate("getcurrent", null, function(d, id) {
			console.log(d);
			console.log(id);
		});
	});

	
	$("#human").on('click', function() {
		isactive.removeClass('active');
		isactive = $("#human");
		isactive.addClass('active');
		$('#myCanvas').annotate("changecolor", 'red', function(d) {
			//console.log(d);
		});
	});

	$("#car").on('click', function() {
		//console.log("car");
		isactive.removeClass('active');
		isactive = $("#car");
		isactive.addClass('active');
		$('#myCanvas').annotate("changecolor", 'blue', function(d) {
			//console.log(d);
		});
	});

	$("#sign").on('click', function() {
		isactive.removeClass('active');
		isactive = $("#sign");
		isactive.addClass('active');
		$('#myCanvas').annotate("changecolor", 'green', function(d) {
			//console.log(d);
		});
	});
});