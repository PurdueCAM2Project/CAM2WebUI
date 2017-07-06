$(document).ready(function(){
	var counter = 0;

	var isactive = $("#human");

	$('#myCanvas').on("annotate-image-added", function(event, id, path){
		$(".my-image-selector").append("<label id=\"" + id + "\"><input type=\"radio\" name=\"image-selector\" class=\"annotate-image-select\" value=\"" + path + "\" checked id=\"" + id + "\"><img src=\"" + path + "\" width=\"35\" height=\"35\"></label>");
	});
	$('#myCanvas').on("annotate-image-remove", function(event, id, path){
		$(".my-image-selector").remove('label#' + id);
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
			$('#myCanvas').annotate("push", {id:"unique_identifier", path: "ftp://128.46.75.58/WD1/2016%20Olympics/01_August_Mon/100_2016-08-01_15-27-14-530185.png"});
			counter += 1;
		}else{
			$('#myCanvas').annotate("push", {id:"unique_identifier", path:"ftp://128.46.75.58/WD1/2016%20Olympics/01_August_Mon/101_2016-08-01_13-44-05-736267.png"});
			
		}
	});


	function objectinfo(d, height, width) {
		var an = [];

		for (var i = 0; i < d.length; i++) {
			var name;
			if (d[i].color === 'red') {
				name = 'human';
			} else if (d[i].color === 'blue') {
				name = 'vehicle';
			} else if (d[i].color === 'green') {
				name = 'street sign'
			}
			var pose = 'Unspecified';
			var truncated = 0;
			var difficult = 0;
			var xmin;
			var xmax;
			var ymin;
			var ymax;
			if (d[i].tox < 0) {
				var xmin = (d[i].fromx + d[i].tox) * width / 640;
				var xmax = d[i].fromx * width / 640;
			} else {
				var xmin = d[i].fromx * width / 640;
				var xmax = (d[i].fromx + d[i].tox) * width / 640;
			}

			if (d[i].toy < 0) {
				var ymin = (d[i].fromy + d[i].toy) * height / 400;
				var ymax = d[i].fromy * height / 400;
			} else {
				var ymin = d[i].fromy * height / 400;
				var ymax = (d[i].fromy + d[i].toy) * height / 400;
			}

			var obj = {
				"name": name,
				"pose": pose,
				"truncated": truncated,
				"difficult": difficult,
				"bndbox": {
					"xmin": xmin,
					"xmax": xmax,
					"ymin": ymin,
					"ymax": ymax
				}
			}
			an.push(obj);
			return an;
		}
	}

	$(".submit-all-images").click(function(event) {
		$('#myCanvas').annotate("getall", null, function(d) {
			console.log(d);
			alert("successful");
		});		
	});

	$(".submit-image").click(function(event) {
		$('#myCanvas').annotate("getcurrent", null, function(d, id, height, width) {
			console.log(d);
			//console.log(id);
			an = objectinfo(d, height, width);

			var o = {"annotation": 
				{"folder": "folder", 
				"filename": "filename",
				"path": id,
				"source": {
						"database": "database"
					},
				"size": {
						"width": width,
						"height": height,
						"depth": 0,
					},
				"segmented": 0,
				"object": an
				}
			}
			console.log(JSON.stringify(o));

			var x2js = new X2JS();
			console.log(x2js.json2xml_str(o));

			alert("successful");

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