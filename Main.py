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
import board
from neopixel import NeoPixel
import os

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

#create LED instance
led = NeoPixel(board.D12, 1)
statuses = {"idle":(255, 255, 255), "error":(255,0,0), "fatal":(255,255,0), "in":(0,255,0), "out":(0,0,255), "off":(0,0,0)}

if debug: print("variables loaded")

#open log file
with open("/home/patribots/PatribotsSignIn/log.csv", "a") as log:
    pass

if debug: print("loaded log file")

#----------------------------------------------------------------------------------------#
#connect to spreadsheet

# define the scope
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/patribots/PatribotsSignIn/roboticsrfidsignin.json", scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open("Test")

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
        return id
    except Exception as e:
        if debug: print(e)
        return None

#send data to spreadsheet
def sendData(id, time):
    sheet_instance.update("A2:B2", [[int(id), int(time)*1000]])

#log id to csv file
def logID(id, is_sign_in):
    with open ("/home/patribots/PatribotsSignIn/log.csv", "a") as log:
        is_sign_in = 1 if is_sign_in else 0
        if debug: print(f"is_sign_in (in log): {is_sign_in}")
        log.write(str(id).strip() + "," + str(time.time()).strip() + "," + str(is_sign_in) + "\n")

#play the sign in chime
def signOutChime():
    if debug: print("chimeOut")
    buzzer.start(90)
    buzzer.ChangeFrequency(809) #this is an A (one octave up than the other notes)
    time.sleep(chimeSpeed)
    buzzer.ChangeFrequency(523) #this is a C
    time.sleep(chimeSpeed)
    buzzer.stop()

#play the sign out chime
def signInChime():
    if debug: print("chimeIn")
    buzzer.start(90)
    buzzer.ChangeFrequency(523) #this is a C
    time.sleep(chimeSpeed)
    buzzer.ChangeFrequency(784) #this is a G
    time.sleep(chimeSpeed)
    buzzer.stop()

#play the error chime
def errorChime():
    if debug: print("errorChime")
    for i in range(3):
        buzzer.start(90)
        buzzer.ChangeFrequency(523)
        time.sleep(chimeSpeed)
        buzzer.stop()
        time.sleep(chimeSpeed)
    

#checks if the user is signing in or out
def isSignIn(id):
    log = np.genfromtxt("/home/patribots/PatribotsSignIn/log.csv", delimiter=",")
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
    
#Sets the LED to whatever status is passed in
#Valid Statuses: "idle, error, fatal, sign in, sign out"
def setLED(status):
    status = status.lower()
    #make sure status is a string
    if type(status) != str:
        raise TypeError("Status must be a string")
    #make sure status is a valid status
    try:
        statuses[status]
    except KeyError as e:
        raise ValueError("Invalid status passed to setLED")
    led[0] = statuses[status]

if debug: print("functions loaded")

#----------------------------------------------------------------------------------------#

#main function
def main():
    lastID = None
    while True:
        try:
            setLED("idle")

            #turn off LED if KeyboardInterrupt is detected
            try:
                id = readCard()
            except KeyboardInterrupt:
                setLED("off")

            try:
                #make sure that the read did not fail
                int(id)
                try:
                    #check to see if the cooldown for an id has expired
                    try:
                        #check if the card has been scanned in the last 60 seconds
                        if time.time() - cache[int(id)] < 60:
                            if debug: print("id on cooldown")
                            setLED("error")
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
                            setLED("in")
                            signInChime()
                        else:
                            setLED("out")
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
                    setLED("error")
            except ValueError:
                errorChime()
                setLED("error")
                continue
        except Exception as e:
            #Sets LED to fatal and saves the error to an error log for later debugging
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            with open("/home/patribots/PatribotsSignIn/errors.csv", "a") as errorLog:
                errorLog.write(str(exc_type) + "," + str(fname) + "," + str(exc_tb.tb_lineno) + "," + str(e) + "\n")
            setLED("fatal")
            errorChime()
            raise SystemExit(str(exc_type) + "," + str(fname) + "," + str(exc_tb.tb_lineno) + "," + str(e) + "\n")

        try:
            if debug: print("#-----------------------------------------#")
        except KeyboardInterrupt:
            setLED("off")
            
        
            
if debug: print("reading")

if __name__ == "__main__":
    main()
