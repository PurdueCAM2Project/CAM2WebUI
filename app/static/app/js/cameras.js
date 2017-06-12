var tableId = "1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg";
var locationColumn = "col1";

function initialize() {
    google.maps.visualRefresh = true;

    var isMobile = (navigator.userAgent.toLowerCase().indexOf('android') > -1) ||
        (navigator.userAgent.match(/(iPod|iPhone|iPad|BlackBerry|Windows Phone|iemobile)/));
    if (isMobile) {
        var viewport = document.querySelector("meta[name=viewport]");
        viewport.setAttribute('content', 'initial-scale=1.0, user-scalable=no');
    }

    var mapDiv = document.getElementById('mapCanvas');
    // mapDiv.style.width = isMobile ? '100%' : '500px';
    // mapDiv.style.height = isMobile ? '100%' : '300px';

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

    google.maps.event.addDomListener(window, 'load', initialize);
  }

function updateMap_Country(layer, tableId, locationColumn, map) {

    document.getElementById('state').innerHTML = '<option value="" selected="selected"> - All - <\/option>';
    document.getElementById('city').innerHTML = '<option value="" selected="selected"> - All - <\/option>';

    var selected = document.getElementById('country');
    var country = selected.value;
    var country_name = selected.options[selected.selectedIndex].text;

    if(selected.selectedIndex > 0) {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode( {'address' : country_name}, function(results, status) {
            while (status != google.maps.GeocoderStatus.OK) {}
                ///console.log("yeah!!!!!!!!!!!!!!!!!");
            map.setCenter(results[0].geometry.location);
            map.fitBounds(results[0].geometry.viewport);
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

    if(country) {
        getStateNames(country);
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
        getCityNamesbyState();
    }
    else{
        document.getElementById('city').innerHTML = '<option value="" selected="selected"> - All - <\/option>';
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: "col5 = '" + document.getElementById('country').value + "'"
            }
        });
    }

}

function updateMap_City(layer, tableId, locationColumn) {
    var city = document.getElementById('city').value;
    var state = document.getElementById('state').value;
    var country = document.getElementById('country').value;

    if (city) {
        if (state) {
            layer.setOptions({
                query: {
                    select: locationColumn,
                    from: tableId,
                    where: "col4 = '" + state + "' AND  " + "col3 = '" + city + "'"
                }
            });
        }
        else {
            layer.setOptions({
                query: {
                    select: locationColumn,
                    from: tableId,
                    where: "col5 = '" + country + "' AND  " + "col3 = '" + city + "'"
                }
            });
        }
    }
    else if(state) {
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: "col4 = '" + state + "'"
            }
        });
    }
    else{
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: "col5 = '" + country + "'"
            }
        });
    }
}

function getCityNamesbyState() {
    document.getElementById('city').isDisabled = false;
    // set the query using the parameters

    var FT_Query_CityName = "SELECT 'City' " +
        "FROM " + tableId;
    var country = document.getElementById('state').value;

    if (country) {
        FT_Query_CityName += " WHERE 'State' = '" + country + "' ";
    }
    FT_Query_CityName += " group by 'City'";

    var queryText = encodeURIComponent(FT_Query_CityName);
    var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);

    //set the callback function
    query.send(createCityDropdown);
}

function getCityNames() {
    document.getElementById('city').isDisabled = false;

    // set the query using the parameters
    var FT_Query_CityName = "SELECT 'City' " +
        "FROM " + tableId;
    var country = document.getElementById('country').value;
    if (country) {
        FT_Query_CityName += " WHERE 'Nation' = '" + country + "' ";
    }
    FT_Query_CityName += " group by 'City'";

    var queryText = encodeURIComponent(FT_Query_CityName);
    var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);

    //set the callback function
    query.send(createCityDropdown);
}

function createCityDropdown(response) {
    if (!response) {
        alert('no response');
        return;
    }
    if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
        return;
    }
    //for more information on the response object, see the documentation
    //http://code.google.com/apis/visualization/documentation/reference.html#QueryResponse
    numRows = response.getDataTable().getNumberOfRows();
    numCols = response.getDataTable().getNumberOfColumns();

    var countryNames = {};
    for (var i = 0; i < numRows; i++) {
        var countryName = response.getDataTable().getValue(i,0);
        // countryName = countryName.substring(0,countryName.indexOf('('));
        countryNames[countryName] = countryName;
    }
    var countryNameDropdown = "<select name='country_select' onchange='handleSelected(this)'>"
    countryNameDropdown += '<option value="" selected="selected"> - All - <\/option>';
    for (countryName in countryNames) {
        countryNameDropdown += "<option value='"+countryName+"'>"+countryName+"</option>"
    }
    countryNameDropdown += "</select>"
    document.getElementById('city').innerHTML = countryNameDropdown;
}

function getStateNames(country) {
    // set the query using the parameters
    if(country != "USA" && country != "CA"){
        getCityNames();
    }
    else {
        document.getElementById('city').isDisabled = true;
        var FT_Query_StateName = "SELECT 'State' " +
            "FROM " + tableId;
        var country = document.getElementById('country').value;
        if (country) {
            FT_Query_StateName += " WHERE 'Nation' = '" + country + "' ";
        }
        FT_Query_StateName += " group by 'State'";

        var queryText = encodeURIComponent(FT_Query_StateName);
        var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);

        //set the callback function
        query.send(createStateDropdown);
    }
}

function createStateDropdown(response) {
    if (!response) {
        alert('no response');
        return;
    }
    if (response.isError()) {
        alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
        return;
    }
    //for more information on the response object, see the documentation
    //http://code.google.com/apis/visualization/documentation/reference.html#QueryResponse

    numRows = response.getDataTable().getNumberOfRows();
    numCols = response.getDataTable().getNumberOfColumns();

    var countryNames = {};
    for (var i = 0; i < numRows; i++) {
        var countryName = response.getDataTable().getValue(i,0);
        // countryName = countryName.substring(0,countryName.indexOf('('));
        countryNames[countryName] = countryName;
    }
    var countryNameDropdown = "<select name='country_select' onchange='handleSelected(this)'>"
    countryNameDropdown += '<option value="" selected="selected"> - All - <\/option>';
    for (countryName in countryNames) {
        countryNameDropdown += "<option value='"+countryName+"'>"+countryName+"</option>"
    }
    countryNameDropdown += "</select>"
    document.getElementById('state').innerHTML = countryNameDropdown;
}

