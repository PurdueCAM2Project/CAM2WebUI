#Navgation Tabs
##Setup
The following is added in `<head></head>`
```
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
```
##Bootstrap Tabs Html
We need to add functions in `/app/templates/app/index.html`
Tabs are created with `<ul class="nav nav-tabs">`
```
  <ul class="nav nav-tabs">
    <li class="active"><a data-toggle="tab" href="#home"> What is CAM2?</a></li>
    <li><a data-toggle="tab" href="#menu1"> Park CAM</a></li>
    <li><a data-toggle="tab" href="#menu2"> Event CAM</a></li>
    <li><a data-toggle="tab" href="#menu3"> City CAM</a></li>
    <li><a data-toggle="tab" href="#menu4"> Flood Record</a></li>
  </ul>
```
Tab content are shown in the following code.
```
<div id="menu1" class="tab-pane fade">

  <div class="row divide" style="padding-top: 50px;
  padding-bottom: 50px;">
    <div style="width: 80%; margin: auto">
      <div class="col-sm-5 col-sm-push-7">
        <h2 class="divide-heading">CAM² Park Cam</h2>
        <p class="lead">
          <ul class="list-unstyled">
            <li><span style="padding:10px" class="fa fa-paw"></span>Detect wildlife patterns.</li>
            <li><span style="padding:10px" class="fa fa-male"></span>Count the number of people at a specific attraction.</li>
          </ul>
        </p>
      </div>
      <div class="col-sm-5 col-sm-pull-5">
        <div class="embed-responsive embed-responsive-16by9">
          <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/OYksWrQJOpQ?rel=0&controls=1&showinfo=0&vq=hd720&autohide=1"></iframe>
         </div>
      </div>
    </div>
  </div>
  </div>
```
Additionally, for the first tab it is in the class `<class="tab-pane fade in active">`.
