function initialize() {
    google.maps.visualRefresh = true;
    var isMobile = (navigator.userAgent.toLowerCase().indexOf('android') > -1) ||
      (navigator.userAgent.match(/(iPod|iPhone|iPad|BlackBerry|Windows Phone|iemobile)/));
    if (isMobile) {
      var viewport = document.querySelector("meta[name=viewport]");
      viewport.setAttribute('content', 'initial-scale=1.0, user-scalable=no');
    }
    var mapDiv = document.getElementById('mapCanvas');
    //mapDiv.style.width = isMobile ? '100%' : '500px';
    //mapDiv.style.height = isMobile ? '100%' : '300px';
    var map = new google.maps.Map(mapDiv, {
      center: new google.maps.LatLng(40.363489, -98.832955),
      zoom: 4,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    layer = new google.maps.FusionTablesLayer({
      map: map,
      heatmap: { enabled: false },
      query: {
        select: "col1",
        from: "1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg",
        where: ""
      },
      options: {
        styleId: 2,
        templateId: 2
      }
    });
    /*
    var column = layer.setOptions({
      query: {
        select: "Nation",
        from: "1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg",
        groupby: "Nation"
      }
    });
    
    console.log(column);
    */
    if (isMobile) {
      var legend = document.getElementById('googft-legend');
      var legendOpenButton = document.getElementById('googft-legend-open');
      var legendCloseButton = document.getElementById('googft-legend-close');
      legend.style.display = 'none';
      legendOpenButton.style.display = 'block';
      legendCloseButton.style.display = 'block';
      legendOpenButton.onclick = function() {
        legend.style.display = 'block';
        legendOpenButton.style.display = 'none';
      }
      legendCloseButton.onclick = function() {
        legend.style.display = 'none';
        legendOpenButton.style.display = 'block';
      }
    }
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

function start() {
  gapi.client.init({
    'apiKey': 'AIzaSyBAJ63zPG5FpAJV9KXBJ6Y1bLKkvzYmhAg',
    'discoveryDocs': ['https://people.googleapis.com/$discovery/rest'],
    'clientId': "143429239389-psh4a8i75tfm2545h2j582ieqc8fndbu.apps.googleusercontent.com",
    'scope': 'profile'
  }).then(function() {
    return gapi.client.people.people.get({
      'resourceName': 'people/me',
      'requestMask.includeField': 'person.names'
    });
  }).then(function(response) {
    console.log(response.result);
  }, function(reason) {
    console.log('Error: ' + reason.result.error.message);
  });
};