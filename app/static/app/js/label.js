$(document).ready(function(){
	var counter = 0;

	var isactive = $("#human");

	var allimg;

	$.get( "/label/getimg", function( data ) {
	  	allimg = JSON.parse(data.list)
	  	//console.log(allimg)
	});

	$('#myCanvas').on("annotate-image-added", function(event, id, path){
		$(".my-image-selector").append("<label id=\"" + id + "\"><input type=\"radio\" name=\"image-selector\" class=\"annotate-image-select\" value=\"" + path + "\" checked id=\"" + id + "\"><img src=\"" + path + "\" width=\"35\" height=\"35\"></label>");
	});
	$('#myCanvas').on("annotate-image-remove", function(event, id){
		$('label#' + id).remove();
	});
	var options = {
		width: "640",          // Width of canvas
  		height: "400",         // Height of canvas
		color: 'red',
		bootstrap: true,
		images: ['ftp://128.46.75.58/WD1/2016%20Olympics/01_August_Mon/161_2016-08-01_15-27-17-440411.png'],
		selectEvent: "change", // listened event on .annotate-image-select selector to select active images
  		unselectTool: true,   // Add a unselect tool button in toolbar (useful in mobile to enable zoom/scroll)
	}


	$('#myCanvas').annotate(options);



	$(".push-new-image").click(function(event) {
		if (counter < allimg.length - 1) {
			var path = allimg[counter + 1]		
			$('#myCanvas').annotate("push", {id:"unique_identifier", path: path});
			counter += 1;
		} else {
			alert('maximum photo')
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
			
		}
		return an;
	}

	$(".submit-all-images").click(function(event) {
		$('#myCanvas').annotate("getall", null, function(d) {
			//console.log(d);
			var all = [];
			var zip = new JSZip();
			var x2js = new X2JS();
			for (var i = 0; i < d.length; i++) {
				var an = objectinfo(d[i].storedElement, d[i].height, d[i].width);
				var o = {"annotation": 
					{"folder": "folder", 
					"filename": "filename",
					"path": d[i].path,
					"source": {
							"database": "database"
						},
					"size": {
							"width": d[i].width,
							"height": d[i].height,
							"depth": 0,
						},
					"segmented": 0,
					"object": an
					}
				}
				zip.file(d[i].id + ".xml", x2js.json2xml_str(o));
				//all.push(o);


			}

			

			zip.generateAsync({type:"blob"})
			.then(function(content) {
			    // see FileSaver.js
			    saveAs(content, "xmlfiles.zip");
			});
			


		});		


		$('#myCanvas').annotate("removeall", null, function() {
			$('#myCanvas').annotate("push", {id:"unique_identifier", path: "ftp://128.46.75.58/WD1/2016%20Olympics/01_August_Mon/119_2016-08-01_15-27-14-993698.png"});
		});	


	});

	$(".submit-image").click(function(event) {
		$('#myCanvas').annotate("getcurrent", null, function(d, path, height, width) {
			console.log(d);
			//console.log(id);
			var an = objectinfo(d, height, width);

			var o = {"annotation": 
				{"folder": "folder", 
				"filename": "filename",
				"path": path,
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

			//alert("successful");
			var blob = new Blob([x2js.json2xml_str(o)], {type: "text/plain;charset=utf-8"});
			saveAs(blob, path + ".xml");

		});


		$('#myCanvas').annotate("removecurrent", null, function() {
			$('#myCanvas').annotate("push", {id:"unique_identifier", path: "ftp://128.46.75.58/WD1/2016%20Olympics/01_August_Mon/119_2016-08-01_15-27-14-993698.png"});
		});
	});

	$(".remove-image").click(function(event) {
		if (counter == 0) {
			alert('last image');
		} else {
			$('#myCanvas').annotate("removecurrent", null, function() {
			});
		}	
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