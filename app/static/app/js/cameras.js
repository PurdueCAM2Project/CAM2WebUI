//Javascript code to display camera database on map
//Authors: Deeptanshu Malik, Juncheng Tang

//functions named updateMap_* are used to update the map based on form inputs from webpage
//functions named get* are used to query data from fusion tables
//function populate_dropdown is used to parse data from JSON object obtained by queries sent from get* functions
//--------------------------------------------------------------------------------------------------------------

//tableId - unique id of database fusions table
//col1 - column containing latitude information for camera
//col2 - column containing longitude information for camera
//col3 - city column
//col4 - state column
//col5 - nation column
var tableId = "1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg";
var locationColumn = "col1";

//Data is obtained from fusion tables by SQL queries
//These queries are sent using HTTP GET requests and a JSON object is returned by fusion tables
//Each query has 3 parts - a url head, the SQL query(encoded as a URL string) and the query tail
//The link below can be referred to understand this further
//https://stackoverflow.com/questions/21497573/fusion-tables-calling-the-api-from-a-browser-using-javascript-uncaught-typee/21511325#21511325

//Note: the callback function's name must be appended as a string to queryTail
//The callback function will be a method to parse the returned JSON object

var queryUrlHead = 'https://www.googleapis.com/fusiontables/v2/query?sql=';
var queryUrlTail = '&key=AIzaSyBAJ63zPG5FpAJV9KXBJ6Y1bLKkvzYmhAg&callback=';

//a global variable to track whether state or city data is to be queried from database fusiontable
var region = '';

//This function is called every time the cameras webpage is loaded
//It initializes a map, overlays a "layer" of data from fusiontables (camera markers) on the map
//and uses DOM properties to track user actions on the webpage
window.initialize = function() {

    //the code below to initialize map and populate markers on map is obtained using the 'publish' tool from fusiontables
    google.maps.visualRefresh = true;

    var isMobile = (navigator.userAgent.toLowerCase().indexOf('android') > -1) ||
        (navigator.userAgent.match(/(iPod|iPhone|iPad|BlackBerry|Windows Phone|iemobile)/));
    if (isMobile) {
        var viewport = document.querySelector("meta[name=viewport]");
        viewport.setAttribute('content', 'initial-scale=1.0, user-scalable=no');
    }

    var mapDiv = document.getElementById('mapCanvas');

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

    //country, state and city are names for html select tags for the corresponding dropdown menus on html webpage
    //layer - to update data layer from fusion tables according to user requests
    //to understand the code in updateMap* functions - to understand how the map is updated
    //https://developers.google.com/fusiontables/docs/samples/change_query
    google.maps.event.addDomListener($("#country").on("change", function() {
        updateMap_Country(layer, map);
    }));

    google.maps.event.addDomListener($("#state").on("change", function() {
        updateMap_State(layer);
    }));

    google.maps.event.addDomListener($("#city").on("change", function() {
        updateMap_City(layer);
    }));

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
}

//this funciton formulates and passes queries to updateLayer function based on form inputs on cameras webpage
//See this link for API documentation of formulating query: https://developers.google.com/fusiontables/docs/v2/using#queryData
//See this link for example of how to query fusion table: https://developers.google.com/fusiontables/docs/samples/change_query
function updateMap_Country(layer, map) {

    //intialise state and city drop down menus to NULL values when no country is selected
    var selected = document.getElementById('country');
    var country = $("#country").select2('val');

    var co = '(';
    for (var i = country.length - 1; i > 0; i--) {
        co += "'" + country[i] + "'" + ','
    }
    co += "'" + country[0] + "'" + ')'
    if (country.length > 0) {
        var country_name = $("#country").select2('data')[0].text;
    }
    
    //console.log(country_name)
    //if an option other than All is selected from the country dropdown menu then
    //recenter map and zoom in on selected country
    //to do so send a geocoding request - as explained below
    //https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple?csw=1
    if(country.length == 1) {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode( {'address' : country_name}, function(results, status) {
            while (status != google.maps.GeocoderStatus.OK) {}
            map.setCenter(results[0].geometry.location);
            map.fitBounds(results[0].geometry.viewport);
        });
        updateLayer(layer, "col5 IN " + co);
    }
    //else recenter on world
    else{
        map.setCenter(new google.maps.LatLng(40.363489, -98.832955));
        map.setZoom(2);
        updateLayer(layer, "");
    }

    //if a country has been selected from the dropdown menu then
    //query database for camera data in its states and city data
    if(country) {
        getStateNames(country);
    }
}

//this funciton formulates and passes queries to updateLayer function based on form inputs on cameras webpage
//See this link for API documentation of formulating query: https://developers.google.com/fusiontables/docs/v2/using#queryData
//See this link for example of how to query fusion table: https://developers.google.com/fusiontables/docs/samples/change_query
function updateMap_State(layer) {
    //parse data from drop down menu to format a string in the required format for a SQL query
    var state = $("#state").select2('val');

    //if a state other than NULL state is selected then populate markers for cameras only in that state
    //otherwise populate markers for cameras only in thae selected country
    console.log(state);
    if(state && state != "NULL") {
        updateLayer(layer, "col4 IN " + getdata_dropdown("#state"));
        getCityNames();
    }
    else{
        //document.getElementById('city').innerHTML = '<option value="" selected="selected"> - All - <\/option>';
        var country = $("#country").select2('val');

        var co = '(';
        for (var i = country.length - 1; i > 0; i--) {
            co += "'" + country[i] + "'" + ','
        }
        co += "'" + country[0] + "'" + ')'

        document.getElementById('city').innerHTML = '<option value="" selected="selected"> - All - <\/option>';
        updateLayer(layer, "col5 IN " + co);
    }
}

//this funciton formulates and passes queries to updateLayer function based on form inputs on cameras webpage
//See this link for API documentation of formulating query: https://developers.google.com/fusiontables/docs/v2/using#queryData
//See this link for example of how to query fusion table: https://developers.google.com/fusiontables/docs/samples/change_query
function updateMap_City(layer) {

    var country = $("#country").select2('val');

    var co = '(';
    for (var i = country.length - 1; i > 0; i--) {
        co += "'" + country[i] + "'" + ','
    }
    co += "'" + country[0] + "'" + ')'
    //var country = document.getElementById('country').value;
    var city = getdata_dropdown("#city");
    var state = getdata_dropdown("#state");

    //if atleast one city has been selected
    //if atleast one state has been selected
    if (city != "('')" && city != "('undefined')") {
        //if atleast one state has been selected
        if (state != "('')" && state != "('undefined')") {
            updateLayer(layer, "col4 IN " + state + " AND  " + "col3 IN " + city);
        }
        else {
            updateLayer(layer, "col5 IN" + co + " AND  " + "col3 IN " + city);
        }
    }
    else{
        updateLayer(layer, "col5 IN " + co);
    }
}

//layer -> fusion tables layer on map to update
//filtering_condition -> a SQL like query to obtained filtered data from fusiontables
//See this link for API documentation of formulating query: https://developers.google.com/fusiontables/docs/v2/using#queryData
//See this link for example of how to query fusion table: https://developers.google.com/fusiontables/docs/samples/change_query
function updateLayer(layer, filtering_condition){
    layer.setOptions({
        query: {
            select: locationColumn,
            from: tableId,
            where: filtering_condition
        }
    });
}

//parse data from drop down menu to format a string in the required format for a SQL query
function getdata_dropdown(dropdown_name){
    var data_array = $(dropdown_name).select2('val');
    var data = '(';
    for (var i = data_array.length - 1; i > 0; i--) {
        data += "'" + data_array[i] + "'" + ','
    }
    data += "'" + data_array[0] + "'" + ')'

    return data;
}

//This function 1) updates region and 2) queries fusion tables
function getCityNames() {
    document.getElementById('city').isDisabled = false;
    region = 'city';
    var query = new google.visualization.Query(queryUrlHead + get_querytext('City') + queryUrlTail + "populate_dropdown");
    query.send();
}

//This function
// if USA is the selected country
// 1) updates region and 2)queries fusion tables
// else it calls the getCityNames functions
function getStateNames(country) {
    // set the query using the parameters
    //console.log(country)
    if (country[0] == "USA"){
        //console.log("hello world")
        document.getElementById('state').isDisabled = false;
        document.getElementById('city').isDisabled = true;
        region = 'state';
        var queryText = get_querytext('State');
        var query = new google.visualization.Query(queryUrlHead + queryText + queryUrlTail + "populate_dropdown");
        //console.log(queryText);
        //set the callback function
        query.send();
    }
    else {
        document.getElementById('state').isDisabled = true;
        getCityNames();

        
    }
}

//query fusiontables database using SQL
//set the query from html form as explained here:
//https://developers.google.com/fusiontables/docs/v2/using#queryData
//Tip: use fusiontables website and set filter conitions on data using its user friendly interface
//then use 'publish' tool to see the correct query and thus, understand how to code it
function get_querytext(data){
    //var country = document.getElementById('country').value;
    var state = getdata_dropdown("#state");
    var country = $("#country").select2('val');

    var co = '(';
    for (var i = country.length - 1; i > 0; i--) {
        co += "'" + country[i] + "'" + ','
    }
    // set the query using the parameters
    var FT_Query = "SELECT '" + data + "' " + "FROM " + tableId;

    if(state != "('')"){
        FT_Query += " WHERE 'State' IN " + state;
        console.log(FT_Query);
        console.log(state.value != (''));
    }
    else if (country) {
        if (state.length > 0 || country[0] != "USA") {
            co += "'" + country[0] + "'" + ')';
            FT_Query += " WHERE 'Nation' IN " + co;
        } else {
            //console.log(state.length)
            co = '(';
            for (var i = country.length - 1; i > 1; i--) {
                co += "'" + country[i] + "'" + ','
            }
            co += "'" + country[1] + "'" + ')'
            FT_Query += " WHERE 'Nation' IN " + co;
        }
        
    }
    FT_Query += " group by '" + data + "'";

    //console.log(FT_Query);

    return encodeURIComponent(FT_Query);
}

//function to populate dropdown menus
function populate_dropdown(response) {
    //if the returned JSON object doesn't have a rows keys then it means that an error has occurred
    if (!response.rows) {
        return;
    }

    //number of data items to populate
    numRows = response.rows.length;

    var Names = {};
    for (var i = 0; i < numRows; i++) {
        var name = response.rows[i][0];
        Names[name] = name;
    }

    var dropdown_list = "<select name='data_select' onchange='handleSelected(this)'>"
    dropdown_list += '<option value="" selected="selected"> - All - <\/option>';
    for (name in Names) {
        dropdown_list += "<option value='"+name+"'>"+name+"</option>"
    }
    dropdown_list += "</select>"
    document.getElementById(region).innerHTML = dropdown_list;
}