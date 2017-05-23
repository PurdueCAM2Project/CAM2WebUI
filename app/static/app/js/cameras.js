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


function sendReq() {
    var testing = new XMLHttpRequest();
    testing.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            console.log(JSON.parse(this.responseText));
        }
    };
    testing.open('GET', 'https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyBAJ63zPG5FpAJV9KXBJ6Y1bLKkvzYmhAg', true);
    testing.send();
}

