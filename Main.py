#hostname: patribots-sign-in
#username: patribots
#password: patribots

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import time


# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./roboticsrfidsignin-99cdbd7ce58b.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('Test')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(3)


# get the total number of columns
sheet_instance.col_count
## >> 26


# get the value at the specific cell
# print(sheet_instance.cell(col=1,row=1))
## >> <Cell R2C3 '63881'>

# stime = time.time()
# for i in range(100):
#     sheet_instance.update_cell(3, 1, str(i))
#     print(i)
# etime = time.time()

# ttime = etime - stime
# print("Total time: " + str(ttime))
# sheet_instance.update_cell(4, 1, ("Total time: " + str(ttime)))
sheet_instance.update('A1:C1', [[0,1,2]])


# I found this github repo that has a lot of examples of how to use rfids. I'm not sure if it will work for you, but it's worth a shot.
# https://github.com/AdamLaurie/RFIDIOt -- This one is more complicated but has a lot to it about rfidot 
# https://github.com/phyushin/Rfid_Register -- This one is literally someone who made a rfid sign in and out form
