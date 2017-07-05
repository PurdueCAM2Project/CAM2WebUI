<i> Note: This documentation has been created to aid in the use of Google Fusion Tables in the CAM2 project and therefore, this is not an exhaustive documentation of all features of Google Fusion Tables, that can be found [here](https://developers.google.com/fusiontables/), but only of those features that are relevant/useful for this project.</i>

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
![image](https://drive.google.com/open?id=0Bx6vDx1hyDf0N3drYm4wTFlvQ0k)
The fusion table will have the same visibility as the host google drive folder where it is stored. BY default, it's the google drive folder that was open when when the table was created.



<i> Note: once your fusion table will start  geocoding will start automatically - <u> cancel it </u>. Only 10,000 data items (less than 10% of our camera database as of July 3, 2017) can be geocoded for free in a 24 hours period. Geocoding is not required to create markers for camera locations on a map however it is required for other features described later in this document and hence, the geocoding quota must not be exhausted. </i>

### Filtering data in fusion tables

### Integrating fusion tables with your webpage

### Querying data from fusion tables using Javascript

### Customizing markers' info windows


