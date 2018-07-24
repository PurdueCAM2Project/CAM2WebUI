# Camera Pop Up View

This page is created for documenting how to display the camera metadata stored in the Google Fusion Table and how to format and create a layout for displaying information about a selected camera.

This assumes that a Google Fusion Table and a Fusion Table Layer for the map on the Cameras page is set up already as per the [Google Fusion Tables](https://purduecam2project.github.io/CAM2WebUI/implementationDetail/GoogleFusionTable.html) documentation page.

This view uses a feature in HTML/CSS called a [Modal Box](https://www.w3schools.com/howto/howto_css_modals.asp) that allows for information to be displayed over a page in a box that can be opened by a button press and closed either by a button or by clicking outside of the modal box.

This page will detail the process of creating the Modal Box currently deployed on the live site.

## The Modal Box - cameras.html

Create a div below the div marked with the ID "content". Give this new div an id tag with a descriptive name, and a unique class for styling purposes.

```
<div id="mapModal" class="modal"></div>
```

Within this div create a nested structure for the modal box content. This doesn't need an ID but should have a unique class for styling purposes.

```
<div id="mapModal" class="modal">
  <div class="modal-content"></div>
</div>
```

Within this nested div any desired content or formatting can be placed. Just be sure that within this nested div is another div with a unique ID. This is where the camera information will end up. In the example below, a span intended for use as a "close" button is placed above the div where the camera information will be located.

```
<div id="mapModal" class="modal">
  <div class="modal-content">
    <span class="modalclose">&close;</span>
    <div id=mapModalInfo></div>
  </div>
</div>
```

## Styling the Box - cameras.css

With the modal set up, we can style it in such a way that it takes on a certain appearence. First, the outer div with class "modal". The below style will hide the modal from view (until changed) and fix it's position and sizing to fill the entire window. It also changes its background to be a somewhat transparent black color. This is used to give the modal box the appearance of being an overlay and is what causes the content "underneath" to appear greyed out or darkened.

```
.modal {
  display: none;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}
```

Next, the first nested div. The below style is used for the white box about the size of 50% of the full window that contains the real content of the modal. The lines from `position: fixed;` to `margin-top: 0px;` are used to center the modal box and ensure that its positioning is consistent and pleasant for devices of variable window sizes. Lastly, this css class uses a very simple animation to make the modal box appear smoothly from the top of the screen whenever it appears.

```
.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 50%;
  position: fixed;
  float: left;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  margin-top: 0px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
  animation-name: animatetop;
  animation-duration: 0.4s;
}

@keyframes animatetop {
  from {top: -300px; opacity: 0}
  to {top: 0; opacity: 1}
}
```

Lastly, the close button. The style below makes the span lightly colored until it is hovered over by a user, at which point it takes on a darker appearance. Note that this is simply for style and not for any functionality.

```
.modalclose {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.modalclose:hover, .modalclose:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
```

## Opening and Closing the Modal - cameras.js and cameras.html

Either add this block below the body of the html or add the code within to a connected JavaScript file to create functionality for closing the modal and returning to the base page. The first anonymous function activates after clicking the span that acts as a close button, and the second activates after clicking the translucent black background around the modal box. Both hide the background and the modal box from view, effectively "closing" the box.

```
<script type="text/javascript">
    document.getElementsByClassName("modalclose")[0].onclick = function() {
        document.getElementById('mapModal').style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == document.getElementById('mapModal')) {
            document.getElementById('mapModal').style.display = "none";
        }
    }
</script>
```

Assuming that the Fusion Table Layer is properly set up, add this line below where the layer is instantiated. This will cause the modal to open whenever a marker on the map is clicked.

```javascript
google.maps.event.addListener(layer, 'click', function(e){
            document.getElementById('mapModal').style.display = "block";
});
```

Of course, all that does is open the modal, but there's still no actual content within the box. To place content within the modal, use the additions to the listener from the previous step shown below. Note that to extract information from a specific column for a given row corresponding to the clicked marker, you can use e.row.{COLUMN ID}.value, where {COLUMN ID} should match the name of whatever column contains the desired information. Also, pay close attention to the line starting with `var expandedcamview`. This is where any customized layouts for displaying camera information should be written.

```javascript
google.maps.event.addListener(layer, 'click', function(e){
            var camID = e.row.ID.value;
            var camLink = e.row.Image.value;
            var camLat = e.row.Latitude.value;
            var camLng = e.row.Longitude.value;
            var camCity = e.row.City.value;
            var camState = e.row.State.value;
            var camCountry = e.row.Country.value;
            var camPlace = '';
            if(camCity != null && camCity != "" && camCity != '' && camCity !="Null"){
                camPlace = camPlace + camCity + ', ';
            }
            if(camState != null && camState != "" && camState != '' && camState !="Null"){
                camPlace = camPlace + camState + ', ';
            }
            if(camCountry != null && camCountry != "" && camCountry != '' && camCountry !="Null"){
                camPlace = camPlace + camCountry;
            }
            var expandedcamview = '<div style="margin:auto;"><img src="' + camLink + '" alt="Image Not Available" width="300" style="margin:auto;display:block;width:60%;">' +
                '<p style="text-align:center;word-wrap:break-word;"><b>Camera ID:</b> ' + camID + '</p>' +
                '<p style="text-align:center;">' + camLat + ', ' + camLng + '</p>' +
                '<p style="text-align:center;">' + camPlace + '</p>';
            document.getElementById('mapModalInfo').innerHTML = expandedcamview;
            document.getElementById('mapModal').style.display = "block"; 
});
```

Once the JavaScript for the modal has been written, deploy the site locally to test the functionality of the modal and ensure that information from the Fusion Table is being displayed properly within the modal box.
