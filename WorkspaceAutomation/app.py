########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# READING APP DATA
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import json

# ENV MANAGEMENT
import os

##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# CLI
from .Config import ConfigFunctions
from .WorkspaceManager import WorkspaceFunctions

# REUSABLE FUNCTIONS
from .common import key_generator

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from .__vars__ import settings_paths

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[os.system()]

##### DEFINE MAIN FILES DIRECTORIES
SETTINGS = os.path.join(MAIN_DIRECTORY, "settings.json")
SECRETS = os.path.join(MAIN_DIRECTORY, ".secrets")

########################################
#####  CLASS                       #####
########################################

class App:

    ##### INITIALISE CLASS
    def __init__(self,
        command: str,
        key: str,
        sub_command: str = None,
        **kwargs) -> None:

        self.yes = kwargs.get("yes") or False
        self.key = key
        self.__load_env_variables()
        self.__load_settings()
        
        # Accepted commands
        commands = [
            "create",
            "import",
            "delete",
            "open",
            "publish",
            "move",
            "edit",
            "config"
        ]

        # Sub Commands for config command
        sub_commands = [
            "vscode",
            "languages",
            "folders",
            "api-key",
            "git-user"
        ]

        # Check if the given command exists
        if command not in commands:
            raise CommandNotFound("The given command was not found or not given")

        if command == "main":
            WorkspaceFunctions(
                command=command,
                api_key=self.API_KEY,
                settings=self.settings,
                yes=self.yes,
                kwargs=kwargs
            )

        # Check if the given subcommand exists
        elif sub_command not in sub_commands:
            raise CommandNotFound("The given subcommand was not found or not given")
        
        else:
            with open(SETTINGS, "r+") as f:
                settings = json.load(f)

            config = ConfigFunctions(
                command=command,
                sub_command=sub_commands,
                settings=settings,
                yes=self.yes,
                kwargs=kwargs
            )

            change = config.parameter

            settings[sub_command] = change

            with open(SETTINGS, "r+") as f:
                json.dump(settings, f)

    # Get saved API_KEY
    def __load_env_variables(self) -> None:

        try:
            load_dotenv(SECRETS)
            encrypted_key = os.getenv("API_KEY")
            self.API_KEY = Fernet(key_generator(self.key)).decrypt(encrypted_key).decode()
        except FileNotFoundError:
            raise FileNotFoundError(".secrets file was not found")
        
        else:
            raise PasswordError("Password is incorrect, API KEY could not get decrypted")

    # Get saved settings
    def __load_settings(self) -> None:

        if not os.path.exists(SETTINGS):
            raise FileNotFoundError("Settings file was not found")

        with open(SETTINGS, "r+") as f:
            self.settings = json.load(f)
