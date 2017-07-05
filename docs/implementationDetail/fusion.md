# Google Fusion Table Sync`

This page will walk you through some guides on synchronizing google fusion table. If you have not finished the document [Upload Files to Google Drive](https://purduecam2project.github.io/CAM2WebUI/implementationDetail/drive.html), finish that first and continue to this document.


## Add the script to the spreadsheet

* Now we're ready to add our script to our spreadsheet. Back at your spreadsheet, go to Tools --&gt; Script Editor and paste the following code.

```
/**
 * appsscript script to run in a google spreadsheet that synchronizes its
 * contents with a fusion table by replacing all rows.
 * based on instructions here: 
 * https://htmlpreview.github.io/?https://github.com/fusiontable-gallery/fusion-tables-api-samples/blob/master/FusionTablesSheetSync/docs/reference.html#enabling_advanced_services
 */

// replace with your fusion table's id (from File > About this table)
var TABLE_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXX';

// first row that has data, as opposed to header information
var FIRST_DATA_ROW = 2;

// true means the spreadsheet and table must have the same column count
var REQUIRE_SAME_COLUMNS = true;

/**
 * replaces all rows in the fusion table identified by TABLE_ID with the
 * current sheet's data, starting at FIRST_DATA_ROW.
 */
function sync() {
    var tasks = FusionTables.Task.list(TABLE_ID);  
    // Only run if there are no outstanding deletions or schema changes.
    if (tasks.totalItems === 0) {
        var sheet = SpreadsheetApp.getActiveSheet();
        var wholeSheet = sheet.getRange(1, 1, sheet.getLastRow(), sheet.getLastColumn());
        var values = wholeSheet.getValues();
        if (values.length > 1) {
            var csvBlob = Utilities.newBlob(convertToCsv_(values), 'application/octet-stream');
            FusionTables.Table.replaceRows(TABLE_ID, csvBlob, { isStrict: REQUIRE_SAME_COLUMNS, startLine: FIRST_DATA_ROW - 1 });
            //Browser.msgBox('Replaced ' + values.length + ' rows in your Fusion Table', Browser.Buttons.OK);
        }
    } else {
        Logger.log('Skipping row replacement because of ' + tasks.totalItems + ' active background task(s)');
    }
};

/**
 * converts the spreadsheet values to a csv string.
 * @param {array} data the spreadsheet values.
 * @return {string} the csv string.
 */
function convertToCsv_(data) {
    // See https://developers.google.com/apps-script/articles/docslist_tutorial#section3
    var csv = '';
    for (var row = 0; row < data.length; row++) {
        for (var col = 0; col < data[row].length; col++) {
            var value = data[row][col].toString();
            if (value.indexOf(',') != -1 ||
                value.indexOf('\n') != -1 ||
                value.indexOf('"') != -1) {
                    // Double-quote values with commas, double quotes, or newlines
                    value = '"' + value.replace(/"/g, '""') + '"';
                    data[row][col] = value;
            }
        };
        // Join each row's columns and add a carriage return to end of each row except the last
        if (row < data.length - 1) {
            csv += data[row].join(',') + '\r\n';
        } else {
            csv += data[row];
        };
    };
    return csv;
};

// create menu buttons
function onOpen() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var menuEntries = [{
        name: "Update Fusion Table",
        functionName: "sync"
    }];
    ss.addMenu("Sync Spreadsheet To Fusion Table", menuEntries);
};
```



* On [Line 9] add Fusion Table's Table ID... It can be get from fusion table property.

        // Add the encrypted table ID of the fusion table here
        var TABLE_ID = '17xnxY......';

* **Optional**: if you have multiple header rows, put the row number of the first data row on this [line](https://gist.github.com/chrislkeller/3013360#file-spreadsheet_to_fusion_tables-js-L12):

            var FIRST_DATA_ROW = 2;

* **Optional**: if you want to allow the spreadsheet to have different columns than the table, change the [line 15](https://gist.github.com/chrislkeller/3013360#file-spreadsheet_to_fusion_tables-js-L15) value to "false":

            var REQUIRE_SAME_COLUMNS = true;

* Click save. You will be prompted to give the project a name. "Update Fusion Tables" works. Click the save icon or go to File --&gt; Save.

* Click Resources  --> Developer's Console Project. Enter the Project Number for the project. The project number can be found in [Google IAM & Admin](https://console.developers.google.com/projectselector/iam-admin/iam). Note that project number is not project id, they are not the same thing. The screen shot below is from another tutorial which is just the screen that we can see after we update our project number.

![](http://archives.chrislkeller.com/blog-images/2012/01/developer_console_project.png)

* Click Resources --> Advanced Google Service, find Google fusion table API, Google SpreadSheet API and enable them. If you don't do that, you will get errors: "Referenced error: FusionTables is not defined"

* Reload the spreadsheet and you will see a new menu item next to help. Mine reads "Sync Spreadsheet To Fusion Table." Click the menu item and you will see an option to "Update Fusion Table." Since our file has more than 100 thousand data points in the file, it may cost more than 5 minutes to execute the script. As long as the file is running, you do not need to worry about the script too much. 


## Synchronize the spread sheet

* Click Edit --> Current Project Trigger, then add a new project trigger to the project.

Since we would like to sync the fusion table everytime when spreadsheet is changed, so we choose the option: "sync", "from spreadsheet", "on change" those options. Then for everytime the spreadsheet is changed, it will automatically run the script and sync spreadsheet content to the fusion table!

________

Now we can update the camera location file into the google drive. We will update the spreadsheet in the particular google drive folder using google drive api and then use google app script to synchronize google fusion table from google spreadsheet everytime when google spreadsheet is change. 
