function initialize() {
    var tableId = "1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg";
    var locationColumn = "col1";

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
        select: locationColumn,
        from: tableId
       },
      options: {
        styleId: 2,
        templateId: 2
      }
    });

    google.maps.event.addDomListener(document.getElementById('country'),
        'change', function() {
            console.log("kjldfjklsdfakl;dsa");
            updateMap_Country(layer, tableId, locationColumn);
        });

    google.maps.event.addDomListener(document.getElementById('state'),
        'change', function() {
            updateMap_State(layer, tableId, locationColumn);
        });

    google.maps.event.addDomListener(document.getElementById('city'),
        'change', function() {
            updateMap_City(layer, tableId, locationColumn);
        });

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

function updateMap_Country(layer, tableId, locationColumn) {
    var selected = document.getElementById('country');
    var country = selected.value;
    var country_name = selected.options[selected.selectedIndex].text;
    if(selected.selectedIndex > 0) {
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode( {'address' : country_name}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                layer.setOptions({
                    center: results[0].geometry.location
                });
            }
        });

        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: "col5 = '" + country + "'"
            }
        });
    }
    else{
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,

                where: "col5 = '" + GB + "'"
            }
        });
    }
}

function updateMap_State(layer, tableId, locationColumn) {
    var state = document.getElementById('state').value;
    if(state) {
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: "col4 = '" + state + "'"
            }
        });
    }
}

function updateMap_City(layer, tableId, locationColumn) {
    var city = document.getElementById('city').value;
    if (city) {
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: "col3 = '" + city + "'"
            }
        });
    }
}

google.maps.event.addDomListener(window, 'load', initialize);
