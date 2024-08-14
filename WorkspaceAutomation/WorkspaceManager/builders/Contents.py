########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
from os import chdir, makedirs, system
from os.path import join
from yaspin import yaspin
from shutil import rmtree

########################################
#####  CODE                        #####
########################################

#####  GLOBAL VARIABLES
from ...__vars__ import settings_paths

# MOVE TO SETTINGS PATH
MAIN_DIRECTORY = settings_paths[system()]
chdir(MAIN_DIRECTORY) # CWD

#####  CLASS
class ContentsManager:

    @yaspin(text="Setting up WorkSpace...")
    def __init__(self, action: int, directory: str, name: str, language: str = None) -> None:
        pass