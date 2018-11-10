//Javascript code to allow for dynamic, responsive live slides for the homepage slideshow
//Author: Anirudh Vegesana

(function() {

	// Adjust the relative sizes of the images in the live slide
	$(".liveslide").width((100. / $('.liveslide').length)+"%");

	// Make a resize function to resize the images in the live slide (for responsiveness)
	function resize(ds) {
		// Show a default image while the real image is loading. In the future, this could be changed to a cached version of the camera.
		ds.style.backgroundImage = "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='"+ds.clientWidth+"' height='"+ds.clientHeight+"'><rect width='100%' height='100%' style='fill:gray; fill-opacity: 0.7'/><text x='50%' y='50%' style='fill:lightBlue;' alignment-baseline='middle' text-anchor='middle' font-size='16'><tspan x='50%' dy='.6em'>Loading</tspan><tspan x='50%' dy='1.2em'>"+ds.getAttribute("name")+"</tspan></text></svg>\")";
		console.log(ds.clientWidth + " "+ ds.clientHeight);
		// Reposition image so it is cropped in the correct location
		ds.getElementsByTagName("img")[0].width = ds.clientWidth * 2;
		ds.scrollLeft = ds.getAttribute("dx")/600*(ds.scrollWidth-ds.clientWidth);
		ds.scrollTop = ds.getAttribute("dy")/800*(ds.scrollHeight-ds.clientHeight);
	};

	[].forEach.call(document.getElementsByClassName("liveslide"), function(ds) {
		// Add the resize function to the image load events
		ds.getElementsByTagName("img")[0].onload = resize.bind(null, ds);
	});

	done = false;

	// Add the resize function to the carousel move and window resize events
	$('#carouselExampleIndicators').on('slid.bs.carousel slide.bs.carousel', window.onresize = function(e) {
		// Only trigger on the second slide (index 1)
		var index = $('#carouselExampleIndicators').find(".active").index();
		if (e.target == window || (index === 0 && !done && (done = true))) {
			// Steal forEach from an Array because JS is ugly and won't let you iterate over a HTMLCollection
			[].forEach.call(document.getElementsByClassName("liveslide"), resize);
		}
	});

})();

//An example of how to use this code:
//<div class=liveslide dx=366 dy=410 name="Purdue Memorial Union"><img src="http://128.210.129.12/mjpg/video.mjpg"></div>