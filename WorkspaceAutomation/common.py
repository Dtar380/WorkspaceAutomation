########################################
#####  DOCUMENTATION               #####
########################################

'''

'''

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
def clear(t: int):
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(t)

def key_generator(input: str):
    return base64.urlsafe_b64encode(
        hashlib.md5(input.encode()).hexdigest().encode()
    )