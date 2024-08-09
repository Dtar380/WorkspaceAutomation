########################################
#####  DOCUMENTATION               #####
########################################

'''
Code from https://gist.github.com/mivade/384c2c41c3a29c637cb6c603d4197f9f
'''

########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
from time import sleep
import os

#####  INTERNAL IMPORTS


########################################
#####  CODE                        #####
########################################

#####  FUNCTIONS
def clear(t: int):
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(t)