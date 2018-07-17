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