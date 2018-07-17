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


Now you can see the image in the html file which has a width of 640, height of 400. If you do annotation on the image, you can use a red rectangle box to draw annotations in the images.



## Push New Image

To push new images into the canvas, we need to first create a new button that can trigger the push image process and add a script that can push image in the djaodjin.

```

<button class="push-new-image">Push a new image!</button>

```

```

$(".push-new-image").click(function(event) {		
		$('#myCanvas').annotate("push", {id:"unique_identifier", path: "some_image_url"});		
	});

```

Then this will trigger the script in the plugin. For every image in the canvas, it will record the id, path, image original height and width for the image.


```

pushImage: function(newImage, set, callback) {
      var self = this;
      var id = null;
      var path = null;
      var img = this.img;
      var height;
      var width;      

      function findHHandWW() {
        height = this.height;
        width = this.width;
        
        id = self.generateId(10);

        var image = {
          id: id,
          height: height,
          width: width,
          path: path,
          storedUndo: [],
          storedElement: []
        };
        self.images.push(image);
        if (set) {
          self.setBackgroundImage(image);
        }
        if (callback) {
          callback({
            id: image.id,
            path: image.path
          });
        }
        self.$el.trigger('annotate-image-added', [
          image.id,
          image.path
        ]);
        return true;
      }
      
      if (typeof newImage === 'object') {
        id = newImage.id;
        path = newImage.path;
        img = new Image();
        img.name = path;
        img.onload = findHHandWW;
        img.src = path;
      } else {
        id = newImage;
        path = newImage;
        img = new Image();
        img.name = path;
        img.onload = findHHandWW;
        img.src = path;
      }
      
    }

```

 In the above script, it can also trigger a new function called 'annotate-image-added'. It will add the checkbox of all the images in the html file. We can add this function in the label.js file to add the image checkboxes.

 ```

 $('#myCanvas').on("annotate-image-added", function(event, id, path){
		$(".my-image-selector").append("<label id=\"" + id + "\"><input type=\"radio\" name=\"image-selector\" class=\"annotate-image-select\" value=\"" + path + "\" checked id=\"" + id + "\"><img src=\"" + path + "\" width=\"35\" height=\"35\"></label>");
	});

```

So the above is the whole process of pushing a new image into the canvas.


## Change Label

Since we need to add different labels to different objects, so we need to change the color of our annoatation box everytime we change our label to make the image look clearer.

On the side of our canvas, we can add a label box to change the labels:

```

<ul class="nav nav-pills nav-stacked" style="margin-top:50px;">
	<li class="active" id="human"><a href="#">Human</a></li>
	<li id="car"><a href="#" >Car</a></li>
	<li id="sign"><a href="#" >Street Sign</a></li>
</ul>


```

To change the color of the label box after it is clicked(active), we need to add a new css file to change its color.

```

.nav-pills>li.active#human>a{
   background-color: red !important;
}

.nav-pills>li.active#car>a{
   background-color: blue !important;
}

.nav-pills>li.active#sign>a{
   background-color: green !important;
}


```

Then use jquery functions to change the settings of the annotation box after each click, we add a new funtion in the plugin called 'changecolor' to change the annotation box color:

```

$("#human").on('click', function() {
	isactive.removeClass('active');
	isactive = $("#human");
	isactive.addClass('active');
	$('#myCanvas').annotate("changecolor", 'red', function(d) {
		// callbacks
	});
});

$("#car").on('click', function() {
	//console.log("car");
	isactive.removeClass('active');
	isactive = $("#car");
	isactive.addClass('active');
	$('#myCanvas').annotate("changecolor", 'blue', function(d) {
		// callbacks
	});
});


```

Then there will be a complicated process in djaodjin-annotate to change the color of the annotation box. I have modified some arguments and functions of the original plugin to make the annotation box change its color.


## Submit Image and generate xml file


Just like pushing the images, when we submit image, we need to create button to submit image and create script to trigger the image.

```

<button class="submit-image">Submit Current Image</button>

```

```

$(".submit-image").click(function(event) {
	$('#myCanvas').annotate("getcurrent", null, function(d, id, height, width) {
	
	}
});

```

The callback of the getcurrent function in the plugin will return four elements: storedElements of the annotation box, id of the image, height and width of the image. Then we will use javascript object to create a full object using the data we get.


```

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

```

Since there is no javascript function which can directly change json to xml, so we will use a new library to convert javascript object to xml. We will be using a library called x2js to convert that.

```
<script type="text/javascript" src="https://cdn.rawgit.com/abdmob/x2js/master/xml2json.js"></script>

```

Then we can directly change the js object into the xml data format.


```
var x2js = new X2JS();
console.log(x2js.json2xml_str(o));

```

In our website, we have created another button called submit all images, this will submit all the images that we have pushed in our websites. The functionalities are pretty much similar.


## Download xml and zip files

After we create our xml data, we need to download it after we generate it. We also need to import libraries that allow us to download any file or zip it to download a zip file.

To download a single file, we need to use [https://github.com/eligrey/FileSaver.js/](https://github.com/eligrey/FileSaver.js/)

To download multiple files and zip it, we need to use [https://stuk.github.io/jszip/](https://stuk.github.io/jszip/) 

Follow the instructions on those websites, we can download the single xml file like the following.

```

var blob = new Blob([x2js.json2xml_str(o)], {type: "text/plain;charset=utf-8"});
saveAs(blob, id + ".xml");

```

We can download the zip file for all xml files like the following.

```
for loop {
	zip.file(d[i].id + ".xml", x2js.json2xml_str(o));
}

zip.generateAsync({type:"blob"})
.then(function(content) {
    // see FileSaver.js
    saveAs(content, "xmlfiles.zip");
});

```


## Remove file

After everytime we submit a image, we need to remove the previous image to leave space for new image. So in the last step of submit image, we need to remove image.

We do the reverse step of pushing the image. We will remove the image in the array with current id.

```

removecurrentImage: function(callback) {
  var self = this;
  var id = self.selectedImage;

  for (var i = 0; i < self.images.length; i++) {
    if (self.images[i].id === id) {
      self.images.splice(i, 1);
    }
    //console.log(self.images);
  }

  self.$el.trigger('annotate-image-remove', [
    id
  ]);
}

```

This will also trigger a function in label.js called 'annotate-image-remove'. It is the reverse process of adding the image in the html.


```

$('#myCanvas').on("annotate-image-remove", function(event, id){
	$('label#' + id).remove();
});

```

## Zoom in and out

Sometimes, it is not easy to annotate the image if the object in the image is too small or too large. So I created zoom in and zoom out function to solve with that problem.

We need to notice that everytime we zoom the image, we need to also zoom the stored annotation boxes and change the canvas width. So we can get the correct size for the annotation boxes in the xml files.

```

$(".zoom-in").click(function(event) {
    curr_width = curr_width * 1.25;
    curr_height = curr_height * 1.25;
    $('#myCanvas').annotate("resize", '+', function(){

    });
  });

```

After we change the canvas size, we need to change the annoation box size for every image. We also need to change the undo element size so that undo is also in the correct size. Then we can clear the original image and redraw the image to make the whole image look properly.

```

resize: function(event, cmdOption) {
  var self = this;

  if (cmdOption === '+') {
    self.options.width = self.options.width * 1.25;
    self.options.height = self.options.height * 1.25;
    self.currentWidth = self.currentWidth * 1.25;
    self.currentHeight = self.currentHeight * 1.25;
    self.selectImageSize.width = self.selectImageSize.width * 1.25;
    self.selectImageSize.height = self.selectImageSize.height * 1.25;
  } else {
    self.options.width = self.options.width * 0.8;
    self.options.height = self.options.height * 0.8;
    self.currentWidth = self.currentWidth * 0.8;
    self.currentHeight = self.currentHeight * 0.8;
    self.selectImageSize.width = self.selectImageSize.width * 0.8;
    self.selectImageSize.height = self.selectImageSize.height * 0.8;
  }

  self.baseCanvas.width = self.drawingCanvas.width = self.currentWidth;
  self.baseCanvas.height = self.drawingCanvas.height = self.currentHeight;
  self.baseContext.drawImage(self.img, 0, 0, self.currentWidth,
    self.currentHeight);
  self.$el.css({
    height: self.currentHeight,
    width: self.currentWidth
  });
  if (cmdOption === '+') {        
    
    for (var i = self.images.length - 1; i >= 0; i--) {
      for (var j = self.images[i].storedElement.length - 1; j >= 0; j--) {
        self.images[i].storedElement[j].fromx = self.images[i].storedElement[j].fromx * 1.25;
        self.images[i].storedElement[j].fromy = self.images[i].storedElement[j].fromy * 1.25;
        self.images[i].storedElement[j].tox = self.images[i].storedElement[j].tox * 1.25;
        self.images[i].storedElement[j].toy = self.images[i].storedElement[j].toy * 1.25;
      }
      for (var j = self.images[i].storedUndo.length - 1; j >= 0; j--) {
        self.images[i].storedUndo[j].fromx = self.images[i].storedUndo[j].fromx * 1.25;
        self.images[i].storedUndo[j].fromy = self.images[i].storedUndo[j].fromy * 1.25;
        self.images[i].storedUndo[j].tox = self.images[i].storedUndo[j].tox * 1.25;
        self.images[i].storedUndo[j].toy = self.images[i].storedUndo[j].toy * 1.25;
      }     
    }

  } else {
    
    for (var i = self.images.length - 1; i >= 0; i--) {
      for (var j = self.images[i].storedElement.length - 1; j >= 0; j--) {
        self.images[i].storedElement[j].fromx = self.images[i].storedElement[j].fromx * 0.8;
        self.images[i].storedElement[j].fromy = self.images[i].storedElement[j].fromy * 0.8;
        self.images[i].storedElement[j].tox = self.images[i].storedElement[j].tox * 0.8;
        self.images[i].storedElement[j].toy = self.images[i].storedElement[j].toy * 0.8;
      }
      for (var j = self.images[i].storedUndo.length - 1; j >= 0; j--) {
        self.images[i].storedUndo[j].fromx = self.images[i].storedUndo[j].fromx * 0.8;
        self.images[i].storedUndo[j].fromy = self.images[i].storedUndo[j].fromy * 0.8;
        self.images[i].storedUndo[j].tox = self.images[i].storedUndo[j].tox * 0.8;
        self.images[i].storedUndot[j].toy = self.images[i].storedUndo[j].toy * 0.8;
      }        
    }
  }

```


## FTP browser

To get all the images from the ftp server, we need to create a simple ftp client to get the address of all the urls of images.

Here we will use python to create a ftp browser. We will be using the python default library ftplib to browse the ftp server. The full document of ftplib is on [https://docs.python.org/3.6/library/ftplib.html](https://docs.python.org/3.6/library/ftplib.html)

```

ftp = FTP('128.46.75.58')     # connect to host, default port
ftp.login()
ftp.cwd('WD1')

```

First we will be connecting the the ftp server and visit the working directory WD1 which is the directory which all of our image files are stored.

Then we will go through the working directory which we need and get all the image files in the folder. ftp.nlist() will return an array of all the files(including directories) in the current working directory. In the example below, we can get all the images in the first directory first subdirectory. Then we will create a list of the full addresses of all the images.


```

ftplist = ftp.nlst()
ftp.cwd(ftplist[0])
sub1 = ftp.nlst()
ftp.cwd(sub1[0])
a = ftp.nlst()
out = []

for element in a:
  element = 'ftp://128.46.75.58/WD1/' + ftplist[0] + '/' + sub1[0] + '/' + element
  out.append(element)

```
Then close the ftp client and return the whole address in json.

```
j = json.dumps(out)
ftp.close()
return JsonResponse({'list':j})

```

In the javascript file, we can then simply get the full list of the image address using a simple get.

```
$.get( "/label/getimg", {dir: fd, subdir: sd}, function( data ) {
      allimg = JSON.parse(data.list)
  });

```