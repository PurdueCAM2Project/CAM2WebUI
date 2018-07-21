/**
 * AppsScript script to run in a Google Spreadsheet that synchronizes its
 * contents with a Fusion Table by refetching the spreadsheet.
 * @author WebUI Team @ CAM2
 */

/**
 * Add your table ID in File > Project properties > Script Properties in the script editor
 */
var TABLE_ID;

/**
 * This function is only run to check the script is authorized. Call once manually to add triggers.
 */
function checkAuthorization()
{
    var sheet = SpreadsheetApp.getActive();
   // ScriptApp.newTrigger("myEdit").forSpreadsheet(sheet).onEdit().create();
    ScriptApp.newTrigger("myEdit").forSpreadsheet(sheet).onChange().create();
    ScriptApp.newTrigger("onOpen").forSpreadsheet(sheet).onOpen().create();

    return;
}


/**
 * Event handler for  opening the spreadsheet
 * @param e Event object with following attributes:
 * authMode
 * source
 * triggerUid
 * user
 * @link https://developers.google.com/apps-script/guides/triggers/events
 */
function onOpen(e)
{
  init();
}


/**
 * initializing triggers and menu in spreadsheet
 */
function init(){
  var sheet = SpreadsheetApp.getActive();


  var menuEntries = [{
        name: "Update Fusion Table",
        functionName: "myEdit"
    }];
    sheet.addMenu("Sync Spreadsheet To Fusion Table", menuEntries);

}


/**
 * Event Handler for editing the spreadsheet
 * @param e Event object has the following attributes:
 * authMode
 * oldValue
 * range
 * source
 * triggerUid
 * user
 * value
 * @link https://developers.google.com/apps-script/guides/triggers/events
 */
function myEdit(e){
  Logger.log("change triggered");

  refetch();
  //Logger.log(e);
}


/**
 * Refetches the spreadsheet originally linked to the Fusion table
 * took ~40 secs to refetch 120K records of data
 */
function refetch() {
    try {
        TABLE_ID = PropertiesService.getScriptProperties().getProperty("TABLE_ID");
        if (!TABLE_ID) {

            throw new Error("Add table ID under File > Project properties > Script Properties");
        }
    }
    catch (e) {
        Logger.log(e.message);
        //Browser.msgBox(e.message);
        return;
    }
    if (!TABLE_ID) {
        Logger.log("no table ID");
    }



    try {
        var tasks = FusionTables.Task.list(TABLE_ID);
    }
    catch (e) {
        Logger.log(e.message);
        //Browser.msgBox(e.message.toString());
        return;
    }

    if (tasks.totalItems == 0) {
        FusionTables.Table.refetchSheet(TABLE_ID);
        Logger.log("Done refetching!");
        //Browser.msgBox("Done refetching!");
    }
    else {
        Logger.log("Failed to refetch due to having tasks still running");
    }
}