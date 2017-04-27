function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {
      lat: 40.363489, 
      lng: -98.832955
    }
  });

  var markers = locations.map(function (location, i) {
    return new google.maps.Marker({
      position: location
    });
  });

  // Add a marker clusterer to manage the markers.
  var markerCluster = new MarkerClusterer(map, markers, {
    imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
  });
}
