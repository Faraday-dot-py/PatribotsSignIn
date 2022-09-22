debug = True

if debug: print("program started")
#import dependencies
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import numpy as np
import sys

if debug: print("libraries loaded")

#GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzerPin=13
GPIO.setup(buzzerPin,GPIO.OUT)
buzzer = GPIO.PWM(buzzerPin, 1000)
#Disables those pesky warnings
GPIO.setwarnings(False)

#load variables
reader = SimpleMFRC522()
cache = np.array([])
chimeSpeed = 1

if debug: print("variables loaded")

#open log file
with open('log.csv', 'a') as log:
    pass

if debug: print("loaded log file")

#----------------------------------------------------------------------------------------#

#connect to spreadsheet
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('./roboticsrfidsignin.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('Test')

# get the  sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(2)

#get the log instance of the Spreadsheet
log_instance = sheet.get_worksheet(1)

if debug: print("connected to sheet")

#----------------------------------------------------------------------------------------#

#reader function
def readCard():
    try:
        _, id = reader.read()
        print(id)
        return id
    except Exception as e:
        if debug:print(e)
        return None
    # finally:
    #         GPIO.cleanup()

#send data to spreadsheet
def sendData(id, time):
    sheet_instance.update('A2:B2', [[int(id), int(time)*1000]])
    # print(id)

#log id to csv file
def logID(id):
    with open ('log.csv', 'a') as log:
        log.write(str(id).strip() + ',' + str(time.time()).strip() + '\n')

#check if the id is in the sheet
# def isUpdated(id):
#     lastID = log_instance.cell(2,1).value
#     if int(id) == int(lastID):
#         if debug: print(id)
#         return True
#     return False

#play the sign in chime:
def signInChime():
    if debug: print('chimeIn')
    buzzer.start(90)
    buzzer.ChangeFrequency(809) #this is an A (one octave up than the other notes)
    time.sleep(chimeSpeed)
    buzzer.ChangeFrequency(523) #this is a C
    buzzer.stop()

#play the sign out chime:
def signOutChime():
    if debug: print('chimeOut')
    buzzer.start(90)
    buzzer.ChangeFrequency(523) #this is a C
    time.sleep(chimeSpeed)
    buzzer.ChangeFrequency(784) #this is a G
    buzzer.stop()

#checks if the user is signing in or out <-- Make Better
def isSignIn():
    time.sleep(2)
    # Alexander wonders if the "2,4" is static and should be dynamic
    # or is meant to be that for reasons other than testing
    if log_instance.cell(2,4).value == 'IN':
        return True
    return False
#Better ^
# def isSignIn(UID):
#     ids = sheet.col_values(1)[1:]
#     if debug: print(ids)
#     c = 0
#     for id in ids:
#         if id == UID:

#         c += 1


    

if debug: print("functions loaded")

#----------------------------------------------------------------------------------------#

#main function
def main():
    cache = None
    while True:
        id = readCard()
        if id != cache:
            sendData(id, time.time())
            print("Sent data to spreadsheet")
            logID(id)
            # if debug: print('it worked') if isUpdated(id) else print('it didnt work') <-- This doesn't work
            time.sleep(0.25)
            if isSignIn():
                signInChime()
            else:
                signOutChime()
        time.sleep(1)
        cache = id
            
if debug: print("reading")

if __name__ == "__main__":
    main()
