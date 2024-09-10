########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# READING APP DATA
from pathlib import Path
from cryptography.fernet import Fernet
import json
import os

# ENV MANAGEMENT
import platform

# HTTP REQUESTS
import requests

# CLI LIBRARIES
import inquirer
from yaspin import yaspin

##### INTERNAL IMPORTS
# ERRORS
from ..__errors__ import *

# COMMON
from ..common import key_generator, clear

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from ..__vars__ import code_paths, settings_paths, languages

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[platform.system()]

##### DEFINE MAIN FILES DIRECTORIES
WORKSPACES = os.path.join(MAIN_DIRECTORY, "workspaces.json")
SETTINGS = os.path.join(MAIN_DIRECTORY, "settings.json")
SECRETS = os.path.join(MAIN_DIRECTORY, ".secrets")

########################################
#####  CLASS                       #####
########################################

class ConfigFunctions:

    ##### INITIALISE CLASS
    def __init__(self,
        key: str,
        command: str,
        sub_command: str = None,
        settings: dict = None,
        yes: bool = False,
        **kwargs) -> None:

        # Set-up the class variables
        self.command = command
        self.key = key
        self.settings = settings
        self.yes = yes

        # Accepted commands
        commands = {
            "vscode": self.vscode_type,
            "languages": self.select_languages,
            "directories": self.select_directories,
            "github-user": self.get_github_username,
            "api-key": self.get_api_key
        }

        # If the main command is init run every sub-command
        if self.command == "init":
            self.directories = commands["directories"](kwargs)
            clear(0.5)
            self.languages = commands["languages"](kwargs)
            clear(0.5)
            self.vscode = commands["vscode"](kwargs)
            clear(0.5)
            self.git_user = commands["github-user"](kwargs)
            clear(0.5)
            self.api_key = commands["api-key"](kwargs)
            clear(0.5)

        # If there was a valid subcommand provided is config run the sub-command
        elif sub_command in commands.keys():
            self.parameter = commands[sub_command](kwargs)

        # Else, raise an error
        else:
            raise InvalidSubCommand("The sub-command is not valid or not provided.")

    ##### VSCODE
    # Select VSCode type between insiders and normal
    def vscode_type(self, **kwargs) -> dict:

        # Get the VSCode type and convert it into directory and PATH ENV VARIABLE
        code_type = kwargs.get("vscode") or inquirer.list_input("Select the VSCode type", choices=["code", "insiders"])

        code_dir = "code - insiders" if code_type == "insiders" else "code"
        code_PATH = "code-insiders" if code_type == "insiders" else "code"

        vscode = {
            "type": code_PATH,
            "path": code_paths[platform.system()].format(code_dir)
        }

        # Ask for confirmation
        if self.command != "init" and (not self.yes or not inquirer.confirm("Want to save changes?")):
                print("Exiting...")
                return None

        # Return the VSCode dict with the directory and PATH ENV VARIABLE
        return vscode

    ##### LANGUAGES
    # Select the most used languages by the user
    def select_languages(self, **kwargs) -> list:

        # Get the languages and convert it into a list
        all_languages = languages.keys()

        # Get the preselected languages
        selected_languages = self.settings["languages"] or kwargs.get("set_up_languages") or None

        # Ask the user to select the languages using a checkbox
        question = inquirer.Checkbox(
            name = "languages",
            message = "Select the languages you use",
            choices = all_languages,
            default = selected_languages)

        answer = inquirer.prompt([question])["languages"]

        # Ask for confirmation
        if not self.command != "init" and (not self.yes or not inquirer.confirm("Want to save changes?")):
            print("Exiting...")
            return None

        # Return the selected languages
        return answer

    ##### DIRECTORIES RELATED
    # Get the directories to work on with the workspaces
    def select_directories(self, **kwargs) -> tuple:

        # Get the main directory and if user wants to use existing directories or create new ones
        main_dir = kwargs.get("custom_dir") or Path(Path.joinpath(Path.home(), "Documents"))
        create = kwargs.get("create_directories") or inquirer.confirm("Want to create new directories?", default=False)

        # Raise an error if the main directory was not found
        if not os.path.exists(main_dir):
            raise DirectoryNotFound("Specified directory was not found.")

        # Get the directories in the main directory
        directories = [i.lower() for i in os.listdir(main_dir) if "." not in i]

        # If there are existing directories in main directory and user doesn't want to create new ones
        if directories and not create:
            sub_directories = self.__select_directories(directories=directories)
        else:
            sub_directories = self.__ask_directories()
            self.__create_directories(
                main_dir=main_dir,
                sub_directories=sub_directories)

        # Return main directory and sub directories selected as a tuple
        return main_dir, sub_directories

    # Get user selected directories
    def __select_directories(self, directories) -> list:

        # Set github directory as default if exists
        if "github" in directories:
            default = ["github"]

        # Ask the user to select the directories using a checkbox
        question = inquirer.Checkbox(
            name = "directories",
            message = "Select the directories you want to use",
            choices = directories,
            default = default)

        answer = inquirer.prompt([question])["directories"]

        # Return the selected directories as a list
        return answer

    # Get directories that user wants to create
    def __ask_directories(self, main_directory: str) -> list:

        sub_directories = []

        # Get directories until user wants to stop
        while True:
            folder = inquirer.text(message="Enter the name for the folder")

            # Check if the directory already exists and ask for confirmation
            if os.path.exists(os.path.join(main_directory, folder)):
                print(f"Folder {folder} already exists, enter a new name.")
            elif inquirer.confirm(message=f"Want to create a folder called {folder}?"):
                sub_directories.append(folder)

            if not inquirer.confirm(message="Want to add more directories?"):
                return sub_directories

    # Create the new directories
    @yaspin(text=" Creating directories...")
    def __create_directories(self, main_dir: str, sub_directories: list) -> None:

        # Ask for confirmation
        if not self.command != "init" and (not self.yes or not inquirer.confirm("Want to save changes?")):
            print("Exiting...")
            return None

        # Create directories
        for i in sub_directories:
            os.mkdir(os.path.join(main_dir, i))

    ##### API KEY
    # Get Api Key and return encrypted version
    def get_api_key(self, **kwargs) -> str:

        # Get API Key
        new_key = kwargs.get("api_key") or inquirer.text("Enter your API Key")

        # Verify API Key
        headers = {
            "Authorization": "Bearer " + new_key,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        message = requests.get(url="https://api.github.com/repos/Dtar380/WorkspaceAutomator", headers=headers)

        # Raise an error if the API Key was not verified
        if message.status_code == 200:
            print("KEY WAS VERIFIED")
        else:
            raise API_KEY_ERROR(f"Failed verificaion [ERROR CODE: {message.status_code}]")

        # Encrypt API Key using password provided by user
        encrypted_key = Fernet(key_generator(self.key)).encrypt(new_key.encode()).decode()

        # Ask for confirmation
        if not self.command != "init" and (not self.yes or not inquirer.confirm("Want to save changes?")):
            raise Exception("Exiting...")

        # Return encrypted API Key
        return encrypted_key

    ##### GitHub
    # Get GitHub username
    def get_github_username(self, **kwargs) -> str:

        while True:
            username = kwargs.get("github_user") or inquirer.text("Enter your GitHub username")

            # Ask for confirmation and return username
            if inquirer.confirm(f"Is {username} correct?") and self.__check_github_user(username=username):
                return username

    # Check if github user exists
    def __check_github_user(self, username: str) -> bool:

        if requests.get(f"https://github.com/{username}").status_code != 200:
            print("\nUsername does not exist\n")
            return False

        return True

    ##### SAVE SETTINGS
    # Save the settings
    @yaspin(text=" Saving settings...")
    @classmethod
    def save_settings(cls,
        settings: dict,
        **kwargs
        ) -> None:

        # Modify settings
        if settings:
            if kwargs.get("directories"):
                settings["directories"] = kwargs.get("directories")
            if kwargs.get("languages"):
                settings["languages"] = kwargs.get("languages")
            if kwargs.get("vscode"):
                settings["vscode"] = kwargs.get("vscode")
            if kwargs.get("github-user"):
                settings["github-user"] = kwargs.get("github-user")

        # Create settings
        elif kwargs.keys() == ["directories", "languages", "vscode", "github-user"]:
            settings = kwargs

        # Save and create files
        if settings:
            with open(SETTINGS, "w+") as f:
                json.dump(settings, f)

        if not os.path.exists(WORKSPACES):
            with open(WORKSPACES, "w+") as f:
                pass

        if kwargs.get("api-key"):
            with open(SECRETS, "w+") as f:
                f.write(f'API_KEY = "{kwargs.get("api-key").decode()}"')
