##################################################
#####     IMPORTS                            #####
##################################################

#####  EXTERNAL IMPORTS
# ENV AND PATHS
import os
import platform

##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# CLI
from .Config import ConfigFunctions

##################################################
#####     CODE                               #####
##################################################

from .__vars__ import settings_paths

#####  DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[platform.system()]

##################################################
#####     CLASS                              #####
##################################################

class SetUp:

    def __init__(self,
        key: str,
        **kwargs
        ) -> None:

        # OS of the user
        self.__check_compatibility()

        # Set the yes variable
        self.yes = kwargs.get("yes") or False

        # Check if a setup has already been performed
        if os.path.exists(MAIN_DIRECTORY):
            raise ReSetupError("Cannot re-setup, maybe you rather run '-c config -sc <sub_command>' command.")
        else:
            os.makedirs(MAIN_DIRECTORY, exist_ok=True)

        # Create the config values
        config = ConfigFunctions(
            key=key,
            command="init",
            yes=self.yes,
            kwargs=kwargs
        )

        # Variables related to settings.json
        self.directories = config.directories
        self.languages = config.languages
        self.vscode = config.vscode
        self.git_username = config.git_user

        # GitHub api key
        self.api_key = config.api_key

        # Save settings to their respective locations
        ConfigFunctions().save_settings(kwargs={
            "directories": self.directories,
            "languages": self.languages,
            "vscode": self.vscode,
            "github-user": self.git_username,
            "api-key": self.api_key
        })

    # Determine if os is compatible
    def __check_compatibility(self) -> None:

        # Compatible OS
        if platform.system() == "Linux":
            return None
        elif platform.system() == "Darwin":
            return None
        elif platform.system() == "Windows":
            return None

        # Incompatibility Error
        else:
            raise NotCompatibleOS("Your OS is not supported.")
