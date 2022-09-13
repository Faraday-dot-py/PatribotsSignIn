import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./roboticsrfidsignin-99cdbd7ce58b.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('Test')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(1)


# get the total number of columns
sheet_instance.col_count
## >> 26


# get the value at the specific cell
# print(sheet_instance.cell(col=1,row=1))
## >> <Cell R2C3 '63881'>

sheet_instance.update_cell(2, 1, "Val1")
sheet_instance.update_cell(2, 2, "Val2")
sheet_instance.update_cell(2, 3, "Val3")