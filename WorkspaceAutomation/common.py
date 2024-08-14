########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
import base64
import hashlib

from time import sleep
import os

########################################
#####  CODE                        #####
########################################

#####  FUNCTIONS
# Clear the screen
def clear(t: int):
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(t)

# Generate a hashlib key for the Fernet class
def key_generator(input: str):
    return base64.urlsafe_b64encode(hashlib.md5(input.encode()).hexdigest().encode())
