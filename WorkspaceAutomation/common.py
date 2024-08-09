########################################
#####  DOCUMENTATION               #####
########################################

'''

'''

########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
from time import sleep
import os

########################################
#####  CODE                        #####
########################################

#####  FUNCTIONS
def clear(t: int):
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(t)