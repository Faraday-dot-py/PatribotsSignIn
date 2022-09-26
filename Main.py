debug = True

if debug: print("program started")
#import dependencies
from ast import Index
from distutils.log import error
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
cache = {}
chimeSpeed = 0.1

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
def logID(id, is_sign_in):
    with open ('log.csv', 'a') as log:
        is_sign_in = 1 if is_sign_in else 0
        if debug: print(f"is_sign_in (in log): {is_sign_in}")
        log.write(str(id).strip() + ',' + str(time.time()).strip() + "," + str(is_sign_in) + '\n')

#check if the id is in the sheet
# def isUpdated(id):
#     lastID = log_instance.cell(2,1).value
#     if int(id) == int(lastID):
#         if debug: print(id)
#         return True
#     return False

#play the sign in chime:
def signOutChime():
    if debug: print('chimeOut')
    buzzer.start(90)
    buzzer.ChangeFrequency(809) #this is an A (one octave up than the other notes)
    time.sleep(chimeSpeed)
    buzzer.ChangeFrequency(523) #this is a C
    time.sleep(chimeSpeed)
    buzzer.stop()

#play the sign out chime:
def signInChime():
    if debug: print('chimeIn')
    buzzer.start(90)
    buzzer.ChangeFrequency(523) #this is a C
    time.sleep(chimeSpeed)
    buzzer.ChangeFrequency(784) #this is a G
    time.sleep(chimeSpeed)
    buzzer.stop()

def errorChime():
    if debug: print('errorChime')
    for i in range(3):
        buzzer.start(90)
        buzzer.ChangeFrequency(523)
        time.sleep(chimeSpeed)
        buzzer.stop()
        time.sleep(chimeSpeed)
    

#checks if the user is signing in or out <-- Make Better
def isSignIn(id):
    log = np.genfromtxt('log.csv', delimiter=',')
    for i in range(len(log)-1, -1, -1):
        try:
            if log[i][0] == id:
                if log[i][2] == 1:
                    return True
                else:
                    return False
        except IndexError as e:
            if debug: print(e)
            return True
    return True
    
        

if debug: print("functions loaded")

#----------------------------------------------------------------------------------------#

#main function
def main():
    lastID = None
    while True:
        id = readCard()
        try:
            #make sure that the read did not fail
            int(id)
            try:
                #check to see if the cooldown for an id has expired
                try:
                    #check if the card has been scanned in the last 60 seconds
                    if time.time() - cache[int(id)] < 60:
                        if debug: print("id on cooldown")
                        errorChime()
                    else:
                        if debug: print("id not on cooldown")
                        raise Exception("All is good, this is just to run the except")

                except Exception:
                    #send data to spreadsheet
                    sendData(id, time.time())
                    if debug: print(f"Sent id {id} to spreadsheet")

                    is_sign_in = isSignIn(int(id))

                    #play the corresponding chime
                    if is_sign_in:
                        signInChime()
                    else:
                        signOutChime()
                    if debug: print("played chime")

                    #log id to csv file
                    logID(id, is_sign_in)
                    time.sleep(0.25)
                    if debug: print("logged id to csv")

                    #update the cache
                    cache[int(id)] = time.time()
                    if debug: print("updated cache")
    
            except Exception as e:
                if debug: print(e)
                errorChime()
        except ValueError:
            errorChime()
            continue
        if debug: print("#-----------------------------------------#")
        
            
if debug: print("reading")

if __name__ == "__main__":
    main()
