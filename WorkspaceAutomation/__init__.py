########################################
#####  DOCUMENTATION               #####
########################################

'''
'''

########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
import importlib.metadata

#####  INTERNAL IMPORTS
from .__main__ import Renderer

########################################
#####  CODE                        #####
########################################

#####  GLOBAL VARIABLES
__version__ = importlib.metadata.version(__package__ or __name__)
__description__ = "A project to help all fellow devs to not waste time in doing the boring and repetitive stuff"
__author__ = "Dtar380"
__license__ = "GPL v3.0"
__status__ = "4 - Beta"