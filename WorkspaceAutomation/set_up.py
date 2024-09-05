########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# ENV AND PATHS
import os
import platform

##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# CLI
from .Config import ConfigFunctions

########################################
#####  GLOBAL VARIABLES            #####
########################################

from .__vars__ import settings_paths

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[platform.system()]

########################################
#####  CLASS                       #####
########################################

class SetUp:

    ##### INITIALISE CLASS
    def __init__(self,
        key: str,
        **kwargs) -> None:

        # OS of the user
        self.__check_compatibility()

        # Check if a setup has already been performed
        if os.path.exists(MAIN_DIRECTORY):
            raise Exception("Cannot re-setup, maybe you rather run 'config --sub-command' command.")
        else:
            os.makedirs(MAIN_DIRECTORY, exist_ok=True)

        config = ConfigFunctions(key=key,
            command="init",
            kwargs=kwargs)

        # Variables related to settings.json
        self.folders = config.folders
        self.languages = config.languages
        self.vscode = config.vscode
        self.git_username = config.git_user

        # GitHub api key
        self.api_key = config.api_key

        # Save settings to their respective locations
        ConfigFunctions().save_settings(
            sub_directories=self.folders,
            languages=self.languages,
            vscode=self.vscode,
            git_username=self.git_username,
            api_key=self.api_key
        )

    # Checks for the OS of the user
    def __check_compatibility(self) -> None:

        # Accepted OS
        if platform.system() == "Linux":
            return None
        elif platform.system() == "Darwin":
            return None
        elif platform.system() == "Windows":
            return None

        # OS was not accepted
        else:
            raise NotCompatibleOS("Not compatible Operating System.")
