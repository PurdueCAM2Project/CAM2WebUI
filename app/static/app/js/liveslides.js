//Javascript code to allow for dynamic, responsive live slides for the homepage slideshow
//Author: Anirudh Vegesana

//Willing to drop IE support: document.currentScript.getAttribute("slides")
$.getJSON(document.scripts[document.scripts.length-1].getAttribute("slides"), function(clf) {
	"use strict";
	
	/////////////////
	// Configuration
	/////////////////
	// Note slideId and slideNum are different. slideNum is the database column. slideId is the JS location in the carousel.
	var slideId = 1;
	var slideNum = 1;
	var maxStreams = 3;
	
	// Build livebox element
	var lb = document.createElement("div");
	lb.id = "livebox";
	lb.style = "width:100vw; height:25.75vw";
	var slide = document.getElementsByClassName('carousel-inner')[0].getElementsByClassName("carousel-item")[--slideId];
	slide.replaceChild(lb, slide.getElementsByTagName("img")[0]);
	
	// Generate the initial seed from the date
	var now = new Date();
	var seed = now.getDate()*24 + now.getHours();
	 
	// Simple random number generator
	function random() {
		return (seed = (seed * 9301 + 49297) % 233280) / 233280;
	}
	
	/**
	 * Shuffles array in place.
	 * From https://stackoverflow.com/a/6274381
	 * @param {Array} a items An array containing the items.
	 */
	function shuffle(a) {
		var j, x, i;
		for (i = a.length - 1; i > 0; i--) {
			j = Math.floor(random() * (i + 1));
			x = a[i];
			a[i] = a[j];
			a[j] = x;
		}
		return a;
	}

//{dx:320, dy:740, sx:450, sy:800, src:"http://69.167.204.51/axis-cgi/mjpg/video.cgi",   still:"http://69.167.204.51/jpg/1/image.jpg",           name:"West Virginia University"},

	// Display random images on the screen and build captions (captions not yet working)
	var lb = document.getElementById("livebox");
	var cl = shuffle(clf).slice(0, maxStreams);
	var captEl = slide.getElementsByClassName("carousel-caption")[0];
	captEl.class += " container";
	// No IE: String.raw`<div class="row"><div class="col"></div><div class="col"></div><div class="col"></div></div>`
	captEl.innerHTML = "<div class=\"row\"><div class=\"col\"></div><div class=\"col\"></div><div class=\"col\"></div></div>";
	captEl.style="text-align: center;";
	var caption = "";
	var captions = captEl.getElementsByClassName("row")[0].getElementsByTagName("div");
	for (var i = 0; i < cl.length; i++) {
		caption += ", " + cl[i].name;
		captions[i].innerText = cl[i].name;
		// No IE: String.raw`<div class=liveslide dx=${cl[i].dx} dy=${cl[i].dy} sx=${cl[i].sx} sy=${cl[i].sy} still=${cl[i].still} name="${cl[i].name}"><img src="${cl[i].src}"></div>`
		lb.innerHTML += "<div class=liveslide dx="+cl[i].dx+" dy="+cl[i].dy+" sx="+cl[i].sx+" sy="+cl[i].sy+" still="+cl[i].still+" name=\""+cl[i].name+"\"><img src=\""+cl[i].src+"\"></div>";
	}
	document.getElementById("welcome"+slideNum).innerText = caption.substring(2);

	// Adjust the relative sizes of the images in the live slide
	$(".liveslide").width((100. / $('.liveslide').length)+"%");

	// Make a resize function to resize the images in the live slide (for responsiveness)
	function resize(ds) {
		if (ds.clientWidth != 0) {
			// Show a default image while the real image is loading. In the future, this could be changed to a cached version of the camera.
			ds.style.backgroundImage = /*"url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='"+ds.clientWidth+"' height='"+ds.clientHeight+"'><rect width='100%' height='100%' style='fill:gray; fill-opacity: 0.7'/><text x='50%' y='50%' style='fill:lightBlue;' alignment-baseline='middle' text-anchor='middle' font-size='16'><tspan x='50%' dy='.6em'>Loading</tspan><tspan x='50%' dy='1.2em'>"+ds.getAttribute("name")+"</tspan></text></svg>\")"*/"url(\""+ds.getAttribute("still")+"\")";
			console.log(ds.clientWidth + " "+ ds.clientHeight);
			// Reposition image so it is cropped in the correct location
			ds.getElementsByTagName("img")[0].width = ds.clientWidth * 2;
			ds.scrollLeft = ds.getAttribute("dx")/ds.getAttribute("sx")*(ds.scrollWidth-ds.clientWidth);
			ds.scrollTop = ds.getAttribute("dy")/ds.getAttribute("sy")*(ds.scrollHeight-ds.clientHeight);
		}
	};

	// Add the resize function to the image load events
	[].forEach.call(document.getElementsByClassName("liveslide"), function(ds) {
		ds.getElementsByTagName("img")[0].onload = resize.bind(null, ds);
	});

	// Add the resize function to the carousel move and window resize events
	var done = false;
	$('#carouselExampleIndicators').on('slid.bs.carousel', window.onresize = function(e) {
		// Only trigger on the second slide (index 1) or when zoomed
		if (e.target == window || (e.to === slideId && !done && (done = true))) {
			// Steal forEach from an Array because JS is ugly and won't let you iterate over a HTMLCollection
			[].forEach.call(document.getElementsByClassName("liveslide"), resize);
		}
	});

});