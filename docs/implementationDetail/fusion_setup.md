#Google Fusion Tables

This documentation has been created to aid in the use of Google Fusion Tables in the CAM2 project and therefore, this is not an exhaustive documentation of all features of Google Fusion Tables, that can be found [here](https://developers.google.com/fusiontables/), but only of those features that are relevant/useful for this project.

### [About fusion tables](https://support.google.com/fusiontables/answer/2571232?hl=en)
 - "Fusion Tables is an experimental data visualization web application to gather, visualize, and share data tables." - About Fusion Tables, https://support.google.com/fusiontables/answer/2571232?hl=en
 - It's a tool for working with tabulated data
 - Fusion tables are created by uploading data tables, for e.g., spreadsheets or CSV files, to Google Drive
 - Advantages of using Google Fusion Tables
   * Filter and summarize across hundreds of thousands of rows
      * As of July 3, 2017 our camera database consists of more than 110,000 cameras and thus, more than 110,000 rows. Using fusion tables allows effecient rendering of our website.
   * We can chart, map, network graph, or use a custom layout for our data - it will always display the latest data values from our table. 
      * We can perform these operations on the fusion tables website itself and then embed the result to our website
      * We can also perform these operations by writing javascript code to post get requests using the fusion tables api
   * Merge two or three tables to generate a single visualization that includes both sets of data
      * This is very relevant for this project - different camera databases can be merged seamlessly because they all have columns of unique camera IDs.
   * We can turn location tables into maps
      * This is the primary reason we started using fusion tables in our project - the cameras data base consists of latitudanal and longitudanal position data for a camera, i.e., location data, and this allows very efficient rendering of our camera location markers on a google map.
   * Excellent API documentation and stackoverflow support community
 
### Creating fusion tables
Before uploading creating fusion tables it is recommended that the tabulated data have 
- Spreadsheets, delimited text files (.csv, .tsv, or .txt), and Keyhole Markup Language files (.kml) to create fusion tables
- Upload tabulated data to google drive
- In Google Drive select 'New' -> 'File' -> 'More' -> 'Google Fusion Tables' -> 'Create and Share'
![image](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/create%20new%20fusion%20table%20.png)
The fusion table will have the same visibility as the host google drive folder where it is stored. BY default, it's the google drive folder that was open when when the table was created.

<i> Note: if your fusion table contains location data, geocoding will start automatically - <u> cancel it </u>. Only 10,000 data items (less than 10% of our camera database as of July 3, 2017) can be geocoded for free in a 24 hours period. Geocoding is not required to create markers for camera locations on a map, however, it is required for other features described later in this document and hence, the geocoding quota must not be exhausted. </i>

### Filtering data in fusion tables
In the example below [this](https://fusiontables.google.com/DataSource?docid=1XszW34wSZP2dW4tfBJxX_Tnvmvvqnumd31WMIlxg#rows:id=1) table is used.

1. Use filter button located on top left of fusion table
![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/filter%20button.png)

2. Filter data using column values.
![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/filter%20by%20columns.png)

3. Multiple filters can be applied - all filter conditions are logically ANDed.
![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/can%20apply%20multiple%20filters.png)
![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/filter%20conditions%20are%20logically%20ANDed.png)

### Getting HTML and Javascript code for map obtained from location data
In our example, we have used a fusion table with location data and consequently, obtained a 'Map of Latitudes'.

1. Navigate to 'Map of Latitudes'.
![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/Map%20of%20Latitudes%20Page.png)
2. Tools -> Publish -> Get HTML and Javascript -> happy copying and pasting :)
![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/Getting%20html%20and%20javascript%20code%20using%20Publish%20tool.png)

### Querying data from fusion tables using Javascript
See this post: https://developers.google.com/fusiontables/docs/samples/change_query

<i> Tip: To understand how to write the query in code - apply the exact filter condition you are trying to code on the fusion table and then see the string displayed on the the right side of the 'Filter' button: </i>
 ![](https://github.com/PurdueCAM2Project/CAM2WebUI/blob/adddocumentation_fusiontables/docs/static/images_for_docs/filter%20conditions%20are%20logically%20ANDed.png)

### Customizing markers' info windows

By default the ma
