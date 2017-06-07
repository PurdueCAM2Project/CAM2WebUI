var tableId = "1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg";
var locationColumn = "col1";

function initialize() {
    //createSidebar();
    //google.setOnLoadCallback(getCityNames);
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
        heatmap: {enabled: false},
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
            updateMap_Country(layer, tableId, locationColumn, map);
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

    google.maps.event.addDomListener(window, 'load', initialize);

// Set a callback to run when the Google Visualization API is loaded.
    //google.setOnLoadCallback(createSidebar);

  }

function updateMap_Country(layer, tableId, locationColumn, map) {

    var selected = document.getElementById('country');
    var country = selected.value;
    var country_name = selected.options[selected.selectedIndex].text;
    //console.log(selected.selectedIndex);
    if(selected.selectedIndex > 0) {
        var geocoder = new google.maps.Geocoder();
        //console.log("yeah???");
        geocoder.geocode( {'address' : country_name}, function(results, status) {
            //console.log("yeah!!!");
            while (status != google.maps.GeocoderStatus.OK) {}
                ///console.log("yeah!!!!!!!!!!!!!!!!!");
            map.setCenter(results[0].geometry.location);
            map.setZoom(4);
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
        map.setCenter(new google.maps.LatLng(40.363489, -98.832955));
        map.setZoom(2);
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId
            }
        });
    }
    //getCityNames(country);
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

// function getCityNames(country) {
//     // set the query using the parameters
//     var FT_Query_CountryName = "SELECT 'col3' FROM "+ tableId +" WHERE 'col5' = '"+ country +"' ORDER by 'col3'";
//     //document.getElementById("FTquery4").innerHTML = FT_Query_CountryName;
//     var queryText = encodeURIComponent(FT_Query_CountryName);
//     var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);
//
//     //set the callback function
//     query.send(createCountryDropdown);
// }
