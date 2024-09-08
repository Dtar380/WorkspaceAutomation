##################################################
#####     IMPORTS                            #####
##################################################

#####  EXTERNAL IMPORTS
# READING APP DATA
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import json

# ENV MANAGEMENT
import os
import platform

##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# CLI
from .Config import ConfigFunctions
from .WorkspaceManager import WorkspaceFunctions

# REUSABLE FUNCTIONS
from .common import key_generator

##################################################
#####     CODE                               #####
##################################################

#####  IMPORT GLOBAL VARIABLES FROM FILE
from .__vars__ import settings_paths

#####  DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[platform.system()]

#####  DEFINE MAIN FILES DIRECTORIES
SETTINGS = os.path.join(MAIN_DIRECTORY, "settings.json")
SECRETS = os.path.join(MAIN_DIRECTORY, ".secrets")

##################################################
#####     CLASS                              #####
##################################################

class App:

    def __init__(self,
        key: str,
        command: str,
        sub_command: str = None,
        **kwargs
        ) -> None:

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
            "directories",
            "api-key",
            "git-user"
        ]

        # Check if the command is a non-config command
        if command in commands.remove("config"):
            WorkspaceFunctions(
                command=command,
                api_key=self.API_KEY,
                settings=self.settings,
                yes=self.yes,
                kwargs=kwargs
            )

        # Check for a sub-command for the config command
        elif command == "config" and sub_command in sub_commands:

            config = ConfigFunctions(
                command=command,
                sub_command=sub_commands,
                settings=self.settings,
                yes=self.yes,
                kwargs=kwargs
            )

            change = config.parameter

            if sub_command == "api-key":
                with open(SECRETS, "w+") as f:
                    f.write(f'API_KEY = "{change.decode()}"')

            elif sub_command:
                self.settings[sub_command] = change

                with open(SETTINGS, "w+") as f:
                    json.dump(self.settings, f)

        # The command given was incomplete or incorrect
        else:
            raise CommandNotFound("The given command was not found or not given. Use --help for more info.")

    # Get saved API_KEY
    def __load_env_variables(self) -> None:

        try:
            load_dotenv(SECRETS)
            encrypted_key = os.getenv("API_KEY")
            self.API_KEY = Fernet(key_generator(self.key)).decrypt(encrypted_key).decode()
        except FileNotFoundError:
            raise FileNotFoundError(".secrets file was not found")

        else:
            raise PasswordError("Password is incorrect, API KEY could not get decrypted. Check if it was correctly typed.")

    # Get saved settings
    def __load_settings(self) -> None:

        if not os.path.exists(SETTINGS):
            raise FileNotFoundError("Settings file was not found.")

        with open(SETTINGS, "r+") as f:
            self.settings = json.load(f)
