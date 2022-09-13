//myFunction() is the name of the function that you will call from the spreadsheet
function myFunction() {
    const cellCordinate = "A2:C2";
    var sheet = SpreadsheetApp.getActiveSheet();
		var cells = sheet.getRange(cellCordinate);
		var values = cells.getValues();
	//loop through values of each cell in cells and console.log
		values.forEach(value => {
			var value = value[0];
			console.log(value);
		});
		var nameCell = "D5";
		sheet.getRange(nameCell).setValue(values);
}

/*

var ss = SpreadsheetApp.getActiveSpreadsheet();
var sheet = ss.getSheets()[0];

var cell = sheet.getRange("B5");
cell.setFormula("=SUM(B3:B4)");

*/