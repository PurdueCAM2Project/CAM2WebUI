# Image Annotation

This introduction will walk you through some guides on how to use image annotation plugin and how to write new functionalities of image annotaion website

## Adding Djaodjin-annotate plugin

There are many open source image annotation plugins that we can use. Here I selected one of the most light weighted plugin: 'djaodjin-annotate' to create our image annotation for our website. Since this library is a jquery plugin, so we need to add jquery first, then add this plugin.


The plugin can be found at [https://github.com/djaodjin/djaodjin-annotate](https://github.com/djaodjin/djaodjin-annotate). It is under MIT license so we need to include license in our files. To watch the demo of the original djaojin plugin, you can visit site [https://djaodjin.com/blog/jquery-plugin-to-annotate-images.blog](https://djaodjin.com/blog/jquery-plugin-to-annotate-images.blog)


## initialize the website

After downloading the library, we first need to include the css and js files that we need to use in html file. We also need to create a new javascript file (label.js) to connect the template file with the plugin file.

```

<!DOCTYPE html>
<html>
<head>
	<meta charset=utf-8 />
	<title></title>
	<link rel="stylesheet" href="{% static "app/css/annotate.css" %}">
</head>
<body>
	<script type="text/javascript" src="//code.jquery.com/jquery-1.11.3.min.js"></script>
	<script src="{% static "app/js/djaodjin-annotate.js" %}"></script>
	<script src="{% static "app/js/label.js" %}"></script>

</body>
</html>

```

Then after we include css and js file in html,we just need to add a div element in body which has an id called 'canvas'.

```

<div id="myCanvas"></div>

```

In the new created script file, we can add a script and include customized options for the plugin to initialize the plugin.

```

var options = {
		width: "640",          // Width of canvas
  		height: "400",         // Height of canvas
		color: 'red',
		bootstrap: true,
		images: ['some_image_url'],
		selectEvent: "change", // listened event on .annotate-image-select selector to select active images
  		unselectTool: true,   // Add a unselect tool button in toolbar (useful in mobile to enable zoom/scroll)
	}

	$('#myCanvas').annotate(options);


```


Now you can see the image in the html file which has a width of 640, height of 400. If you do annotation on the image, you can use a red rectangle box to draw boxes in the images.

