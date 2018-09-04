//Javascript code to display camera database on map
//Authors: Deeptanshu Malik, Juncheng Tang

//functions named updateMap_* are used to update the map based on form inputs from webpage
//functions named get* are used to query data from fusion tables
//function populate_dropdown is used to parse data from JSONP object obtained from fusion tables
//
//see documentation of google fusion tables hosted on team's github pages website to understand how to send queries to
//fusion tables for data, how to update map layers etc.
//
//--------------------------------------------------------------------------------------------------------------
(function () {

    'use strict';

    var tableId = "1MtAPEmSd6BQxuDYo_KYePrBxg-SOA-JiGloEcz6i";//all cameras
    //var tableId = "115-UUNvnJHw2abJinqa2CcRIY2mX7uAC4MhTcPYF";//only good cameras
    var locationColumn = "col2";
    var queryUrlHead = 'https://www.googleapis.com/fusiontables/v2/query?sql=';
    var queryUrlTail = '&key=AIzaSyBAJ63zPG5FpAJV9KXBJ6Y1bLKkvzYmhAg&callback=?';

    //a variable to track whether state or city data has been queried from fusiontable
    var region = '';

    var minZoom = 2;
    var center_of_world, maxNorthEastLat, maxNorthEastLng, maxSouthWestLat, maxSouthWestLng;
    var countries_viewport;
    var states_viewport;
    var actives = false;


    //Initialize a layer on map with markers for all cameras in database
    //Add DOM listeners for inputs on cameras html page
    //
    //Note: code to initialize map and populate markers on map is obtained using the 'publish' tool from fusiontables

    window.initialize = function () {

        google.maps.visualRefresh = true;
        center_of_world = new google.maps.LatLng(0, 0);

        var isMobile = (navigator.userAgent.toLowerCase().indexOf('android') > -1) ||
            (navigator.userAgent.match(/(iPod|iPhone|iPad|BlackBerry|Windows Phone|iemobile)/));
        if (isMobile) {
            var viewport = document.querySelector("meta[name=viewport]");
            viewport.setAttribute('content', 'initial-scale=1.0, user-scalable=no');
        }

        var mapDiv = document.getElementById('mapCanvas');

        var map = new google.maps.Map(mapDiv, {
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        center_on_world(map);

        map.setOptions({ minZoom: minZoom});

        var infoWindow = new google.maps.InfoWindow();
        
        var layer = new google.maps.FusionTablesLayer({
            map: map,
            heatmap: {enabled: false},
            query: {
                select: locationColumn,
                from: tableId
            },
            options: {
                styleId: 2,
                templateId: 3,
                suppressInfoWindows: true
            }
        });
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
                '<p style="text-align:center;word-wrap:break-word;"><div class="row"> <button type="button" class="btn btn-primary mx-auto"  data-toggle="collapse" data-target="#toggleID">Camera ID</button></div><div id="toggleID" class="collapse colentered"><p style="text-align:center;word-wrap:break-word;"> ' +  camID +  '</p></div></p>' +
                '<p style="text-align:center;">' + camLat + ',' + camLng + '</p>' +
                '<p style="text-align:center;">' + camPlace + '</p>';
            document.getElementById('mapModalInfo').innerHTML = expandedcamview;
            document.getElementById('mapModal').style.display = "block"; 

            google.maps.event.addDomListener(document.getElementById('reportthiscam'), 'click', function(){
                document.getElementById('cameraID').value = camID;
                document.getElementById('submit').click();
            });




        });

        document.getElementById('activeFilter').onchange = function () {
            // Use the Select Drop-down menu to filter out cameras that are active and cameras that are not.
            //console.log(this.children[this.selectedIndex].value);

            var city = getdata_dropdown("#city");
            var state = getdata_dropdown("#state");
            var country = getdata_dropdown("#country");

            if(this.children[this.selectedIndex].value == "active"){
                actives = true;
                if(country != "('undefined')"){
                    if (city != "('')" && city != "('undefined')") {
                        if (state != "('')" && state != "('undefined')") {
                            updateLayer(layer, "'Country' IN " + country + " AND  " + "'State' IN " + state + " AND  " + "'City' IN " + city + " AND  " + "'Is Active Video' IN 'TRUE'");
                        }
                        else {
                            updateLayer(layer, "'Country' IN" + country + " AND  " + "'City' IN " + city + " AND  " + "'Is Active Video' IN 'TRUE'");
                        }
                    }
                    else if (state != "('')" && state != "('undefined')"){
                        updateLayer(layer, "'Country' IN " + country + " AND  " + "'State' IN " + state + " AND  " + "'Is Active Video' IN 'TRUE'");
                    }
                    else {
                        updateLayer(layer, "'Country' IN " + country + " AND  " + "'Is Active Video' IN 'TRUE'");
                    }
                } else {
                    updateLayer(layer, "'Is Active Video' IN 'TRUE'");
                }
            } else {
                actives = false;
                if(country != "('undefined')"){
                    if (city != "('')" && city != "('undefined')") {
                        if (state != "('')" && state != "('undefined')") {
                            updateLayer(layer, "'Country' IN " + country + " AND  " + "'State' IN " + state + " AND  " + "'City' IN " + city);
                        }
                        else {
                            updateLayer(layer, "'Country' IN" + country + " AND  " + "'City' IN " + city);
                        }
                    }
                    else if (state != "('')" && state != "('undefined')"){
                        updateLayer(layer, "'Country' IN " + country + " AND  " + "'State' IN " + state);
                    }
                    else {
                        updateLayer(layer, "'Country' IN " + country);
                    }
                } else {
                    updateLayer(layer, "");
                }
            }
        }

        google.maps.event.addDomListener($("#country").on("change", function () {
            updateMap_Country(layer, map);
        }));

        google.maps.event.addDomListener($("#state").on("change", function () {
            updateMap_State(layer, map);
        }));

        google.maps.event.addDomListener($("#city").on("change", function () {
            updateMap_City(layer, map);
        }));

        initialize_countries_viewport();
        initialize_states_viewport();

        if (isMobile) {
            var legend = document.getElementById('googft-legend');
            var legendOpenButton = document.getElementById('googft-legend-open');
            var legendCloseButton = document.getElementById('googft-legend-close');
            legend.style.display = 'none';
            legendOpenButton.style.display = 'block';
            legendCloseButton.style.display = 'block';
            legendOpenButton.onclick = function () {
                legend.style.display = 'block';
                legendOpenButton.style.display = 'none';
            }
            legendCloseButton.onclick = function () {
                legend.style.display = 'none';
                legendOpenButton.style.display = 'block';
            }
        }

        google.maps.event.addDomListener(window, 'load', initialize);
    }

    function initialize_countries_viewport() {
        $.ajax({
            'async': false,
            'global': false,
            'url': "/static/app/json/countries_viewport.json",
            'dataType': "json",
            'success': function (data) {
                countries_viewport = data;
            }
        });
    }
    function initialize_states_viewport() {
        $.ajax({
            'async': false,
            'global': false,
            'url': "/static/app/json/states_viewport.json",
            'dataType': "json",
            'success': function (data) {
                states_viewport = data;
            }
        });
    }

    function updateMap_Country(layer, map) {
        var country = getdata_dropdown("#country");

        if (country != "('undefined')") {
            var countryQuery = "'Country' IN " + country;
            if (actives) {
                countryQuery = countryQuery + " AND  " + "'Is Active Video' IN 'TRUE'";
            }
            updateLayer(layer, countryQuery);
            center_on_selected_countries(map);
            getStateNames();
        }
        else {
            var countryQuery = "";
            if (actives) {
                countryQuery = "'Is Active Video' IN 'TRUE'";
            }
            set_dropdown_null("state");
            set_dropdown_null("city");
            updateLayer(layer, countryQuery);
            center_on_world(map);
        }
    }

    function updateMap_State(layer, map) {
        var state = getdata_dropdown("#state");

        if (state != "('')" && state != "('undefined')") {
            var stateQuery = "'State' IN " + state;
            if (actives) {
                stateQuery = stateQuery + " AND  " + "'Is Active Video' IN 'TRUE'";
            }
            updateLayer(layer, stateQuery);
            center_on_selected_states(map)
            getCityNames();
        }
        else {
            set_dropdown_null("city");
            var country = getdata_dropdown("#country");
            var stateQuery = "'Country' IN " + country;
            if (actives) {
                stateQuery = stateQuery + " AND  " + "'Is Active Video' IN 'TRUE'";
            }
            updateLayer(layer, stateQuery);
            center_on_world(map);
        }
    }

    function updateMap_City(layer, map) {
        var city = getdata_dropdown("#city");
        var state = getdata_dropdown("#state");
        var country = getdata_dropdown("#country");

        if (city != "('')" && city != "('undefined')") {
            if (state != "('')" && state != "('undefined')") {
                var citystateQuery = "'State' IN " + state + " AND  " + "'City' IN " + city;
                if (actives) {
                    citystateQuery = citystateQuery + " AND  " + "'Is Active Video' IN 'TRUE'";
                }
                updateLayer(layer, citystateQuery);

            }
            else {
                var citycountryQuery = "'Country' IN" + country + " AND  " + "'City' IN " + city;
                if (actives) {
                    citycountryQuery = citycountryQuery + " AND  " + "'Is Active Video' IN 'TRUE'";
                }
                updateLayer(layer, citycountryQuery);
            }
        }
        else {
            var cityQuery = "'Country' IN " + country;
            if (actives) {
                cityQuery = cityQuery + " AND  " + "'Is Active Video' IN 'TRUE'";
            }
            updateLayer(layer, cityQuery);
        }
    }

    //return string of selected inputs from drop down menu in the required format for a query to fusion table
    function getdata_dropdown(dropdown_name) {
        var data_array = $(dropdown_name).select2('val');
        var data = '(';
        for (var i = data_array.length - 1; i > 0; i--) {
            data += "'" + data_array[i] + "'" + ','
        }
        data += "'" + data_array[0] + "'" + ')'

        return data;
    }

    //See 'Querying data from fusion tables using Javascript' section of Google Fusion Table docs by CAM2WebUI
    //to understand how to update markers on fusion table layer on map
    function updateLayer(layer, filtering_condition) {
        layer.setOptions({
            query: {
                select: locationColumn,
                from: tableId,
                where: filtering_condition
            }
        });
    }

    //using geocoder to center map on country selected - see link below to for documentation and example
    //https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple?csw=1
    function center_on_selected_countries(map) {
        var selected_countries = $("#country").select2('val');

        //initiliaze with corners of first country
        var curr_country = countries_viewport[selected_countries[0]];
        maxNorthEastLat = curr_country.northeast.lat;
        maxNorthEastLng = curr_country.northeast.lng;
        maxSouthWestLat = curr_country.southwest.lat;
        maxSouthWestLng = curr_country.southwest.lng;


        for (var i = 1; i < selected_countries.length; i++) {
            var country = selected_countries[i];
            curr_country = countries_viewport[country];

            var currNorthEastLat = curr_country.northeast.lat;
            var currNorthEastLng = curr_country.northeast.lng;
            var currSouthWestLat = curr_country.southwest.lat;
            var currSouthWestLng = curr_country.southwest.lng;

            if (maxNorthEastLat < currNorthEastLat)
                maxNorthEastLat = currNorthEastLat;

            if (maxNorthEastLng < currNorthEastLng)
                maxNorthEastLng = currNorthEastLng;

            if (maxSouthWestLat > currSouthWestLat)
                maxSouthWestLat = currSouthWestLat;

            if (maxSouthWestLng > currSouthWestLng)
                maxSouthWestLng = currSouthWestLng;
        }

        var bounds = new google.maps.LatLngBounds();

        bounds.extend(new google.maps.LatLng(maxNorthEastLat, maxNorthEastLng));
        bounds.extend(new google.maps.LatLng(maxSouthWestLat, maxSouthWestLng));

        map.fitBounds(bounds);
    }
    //https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple?csw=1
    function center_on_selected_states(map) {
        var selected_states = $("#state").select2('val');

        //initiliaze with corners of first country
        var curr_state = states_viewport[selected_states[0]];
        maxNorthEastLat = curr_state.northeast.lat;
        maxNorthEastLng = curr_state.northeast.lng;
        maxSouthWestLat = curr_state.southwest.lat;
        maxSouthWestLng = curr_state.southwest.lng;

        for (var i = 1; i < selected_states.length; i++) {
            var state = selected_states[i];
            curr_state = states_viewport[state];

            var currNorthEastLat = curr_state.northeast.lat;
            var currNorthEastLng = curr_state.northeast.lng;
            var currSouthWestLat = curr_state.southwest.lat;
            var currSouthWestLng = curr_state.southwest.lng;

            if (maxNorthEastLat < currNorthEastLat)
                maxNorthEastLat = currNorthEastLat;

            if (maxNorthEastLng < currNorthEastLng)
                maxNorthEastLng = currNorthEastLng;

            if (maxSouthWestLat > currSouthWestLat)
                maxSouthWestLat = currSouthWestLat;

            if (maxSouthWestLng > currSouthWestLng)
                maxSouthWestLng = currSouthWestLng;
        }

        var bounds = new google.maps.LatLngBounds();

        bounds.extend(new google.maps.LatLng(maxNorthEastLat, maxNorthEastLng));
        bounds.extend(new google.maps.LatLng(maxSouthWestLat, maxSouthWestLng));

        map.fitBounds(bounds);
    }

    function center_on_world(map) {
        map.setCenter(center_of_world);
        map.setZoom(minZoom);
    }

    function set_dropdown_null(dropdown_name) {
        $("#" + dropdown_name).select2('val', '[]');
        document.getElementById(dropdown_name).innerHTML = '[]';
    }


    function getStateNames() {
        var country = getdata_dropdown("#country");
        var countrylist = $("#country").select2('val');

        if ($.inArray("USA", countrylist) != -1) {
            document.getElementById('state').isDisabled = false;
            document.getElementById('city').isDisabled = true;
            region = 'state';
            var encodedQuery = get_encodedQuery('State');
            sendRequest(encodedQuery);
        }
        else {
            set_dropdown_null("state");
            document.getElementById('state').isDisabled = true;
            getCityNames();
        }
    }

    function getCityNames() {
        document.getElementById('city').isDisabled = false;
        region = 'city';
        var encodedQuery = get_encodedQuery('City');
        sendRequest(encodedQuery);
    }

    //See 'Querying data from fusion tables using Javascript' section of Google Fusion Table docs by CAM2WebUI
    //to understand how to create queries
    function get_encodedQuery(data) {
        var state = getdata_dropdown("#state");
        var country = getdata_dropdown("#country");

        var FT_Query = "SELECT '" + data + "' " + "FROM " + tableId;

        if (state != "('undefined')" && state != "('')")
            FT_Query += " WHERE 'State' IN " + state;
        else if (country != "('undefined')" && country != "('')")
            FT_Query += " WHERE 'Country' IN " + country;

        FT_Query += " group by '" + data + "'";

        return encodeURIComponent(FT_Query);
    }

    function sendRequest(encodedQuery) {
        $.ajax({
            url: queryUrlHead + encodedQuery + queryUrlTail,
            dataType: 'jsonp',
            success: function (response) {
                populate_dropdown(response);
            }
        });
    }

    function populate_dropdown(response) {
        //if the returnedP JSON object doesn't have a rows keys then it means that an error has occurred
        if (!response.rows) {
            return;
        }

        var numRows = response.rows.length;

        var Names = {};
        for (var i = 0; i < numRows; i++) {
            var name = response.rows[i][0];
            Names[name] = name;
        }

        var dropdown_list = "<select name='data_select' onchange='handleSelected(this)'>"
        for (name in Names) {
            dropdown_list += "<option value='" + name + "'>" + name + "</option>"
        }
        dropdown_list += "</select>"
        document.getElementById(region).innerHTML = dropdown_list;
    }
 
    /*function report_camera(cameraID) {
       document.getElementById('cameraID').value = String(cameraID);
       document.getElementById('contact-us').submit();
    }*/

})();
