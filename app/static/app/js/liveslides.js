//Javascript code to allow for dynamic, responsive live slides for the homepage slideshow
//Author: Anirudh Vegesana

// Note slideId and slideNum are different. slideNum is the database column. slideId is the JS location in the carousel.
!function(slideId, slideNum, maxSlides) {
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

	// Build image JSON
	var clf = [
{dx:206, dy:426, sx:600, sy:800, src:"http://206.140.121.226/axis-cgi/mjpg/video.cgi", still:"http://206.140.121.226/jpg/1/image.jpg",         name:"Cleveland Skyline"},
{dx:296, dy:380, sx:600, sy:800, src:"http://128.210.129.12/mjpg/video.mjpg",          still:"http://128.210.129.12/jpg/1/image.jpg",          name:"Purdue Memorial Union"},
{dx:320, dy:300, sx:600, sy:800, src:"http://97.64.145.7/axis-cgi/mjpg/video.cgi",     still:"http://97.64.145.7/jpg/1/image.jpg",             name:"National Naval Association Museum"},
{dx:320, dy:200, sx:450, sy:800, src:"http://199.20.14.240/axis-cgi/mjpg/video.cgi",   still:"http://images.opentopia.com/cams/12609/big.jpg", name:"Schaumburg Lake"},
{dx:132, dy:120, sx:251, sy:447, src:"http://128.206.143.98/axis-cgi/mjpg/video.cgi",  still:"http://128.206.143.98/jpg/1/image.jpg",          name:"Mizzou School of Journalism"},
{dx:320, dy:740, sx:450, sy:800, src:"http://69.167.204.51/axis-cgi/mjpg/video.cgi",   still:"http://69.167.204.51/jpg/1/image.jpg",           name:"West Virginia University"},
	];

	// Display random images on the screen and build captions (captions not yet working)
	var lb = document.getElementById("livebox");
	var cl = shuffle(clf).slice(0, maxSlides);
	var caption = "";
	with (slide.getElementsByClassName("carousel-caption")[0]) {
		this.class += " container";
		innerHTML = String.raw`<div class="row"><div class="col"></div><div class="col"></div><div class="col"></div></div>`;
		style="text-align: center;";
		var captions = getElementsByClassName("row")[0].getElementsByTagName("div");
	}
	for (var i = 0; i < cl.length; i++) {
		caption += ", " + cl[i].name;
		captions[i].innerText = cl[i].name;
		lb.innerHTML += String.raw`<div class=liveslide dx=${cl[i].dx} dy=${cl[i].dy} sx=${cl[i].sx} sy=${cl[i].sy} still=${cl[i].still} name="${cl[i].name}"><img src="${cl[i].src}"></div>`;
	}
	document.getElementById("welcome"+slideNum).innerText = caption.substring(2);

	// Adjust the relative sizes of the images in the live slide
	$(".liveslide").width((100. / $('.liveslide').length)+"%");

	// Make a resize function to resize the images in the live slide (for responsiveness)
	function resize(ds) {
		with (ds) if (clientWidth != 0) {
			// Show a default image while the real image is loading. In the future, this could be changed to a cached version of the camera.
			style.backgroundImage = /*"url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='"+clientWidth+"' height='"+clientHeight+"'><rect width='100%' height='100%' style='fill:gray; fill-opacity: 0.7'/><text x='50%' y='50%' style='fill:lightBlue;' alignment-baseline='middle' text-anchor='middle' font-size='16'><tspan x='50%' dy='.6em'>Loading</tspan><tspan x='50%' dy='1.2em'>"+getAttribute("name")+"</tspan></text></svg>\")"*/"url(\""+getAttribute("still")+"\")";
			// Reposition image so it is cropped in the correct location
			getElementsByTagName("img")[0].width = clientWidth * 2;
			scrollLeft = getAttribute("dx")/getAttribute("sx")*(scrollWidth-clientWidth);
			scrollTop = getAttribute("dy")/getAttribute("sy")*(scrollHeight-clientHeight);
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

}(1, 1, 3);
