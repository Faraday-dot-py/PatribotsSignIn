print("Another test :)")


# #This reads the RFID tag and prints it to the console
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()

# try:
#         id, text = reader.read()
#         print(id)
#         print(text)
# finally:
#         GPIO.cleanup()


# #This writes the RFID tag and prints it to the console
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()

# try:
#         text = input('New data:')
#         print("Now place your tag to write")
#         reader.write(text)
#         print("Written")
# finally:
#         GPIO.cleanup()
