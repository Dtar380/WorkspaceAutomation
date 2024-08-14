########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# ENV AND PATHS
import os

##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# CLI
from .Config import ConfigFunctions

########################################
#####  GLOBAL VARIABLES            #####
########################################

from .__vars__ import settings_paths

########################################
#####  CLASS                       #####
########################################

class SetUp:

    ##### INITIALISE CLASS
    def __init__(self, **kwargs) -> None:

        # OS of the user
        self.__check_compatibility()

        # Check if a setup has already been performed
        if os.path.exists(settings_paths[os.system()]):
            raise DoubleSetUp("Cannot re-setup, maybe you rather run 'config --sub-command' command.")
        else:
            os.makedirs(settings_paths[os.system()], exist_ok=True)

        config = ConfigFunctions(command="set-up", kwargs=kwargs)

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
    def __check_compatibility(self) -> str:
        if os.system() == "Linux":
            return None
        elif os.system() == "Darwin":
            return None
        elif os.system() == "Windows":
            return None
        else:
            raise NotCompatibleOS("Not compatible Operating System.")
