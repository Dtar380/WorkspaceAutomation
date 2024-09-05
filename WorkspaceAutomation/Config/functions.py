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

        self.key = key
        self.settings = settings
        self.yes = yes

        commands = {
            "vscode": self.vscode_type,
            "languages": self.select_languages,
            "folders": self.select_folders,
            "api-key": self.get_api_key,
            "git-user": self.get_github_username
        }

        if command == "init":
            self.folders = commands["folders"](kwargs)
            clear(0.5)
            self.languages = commands["languages"](kwargs)
            clear(0.5)
            self.vscode = commands["vscode"](kwargs)
            clear(0.5)
            self.git_user = commands["git-user"](kwargs)
            clear(0.5)
            self.api_key = commands["api-key"](kwargs)
            clear(0.5)

        elif command == "config":
            self.parameter = commands[sub_command](kwargs)

    ##### VSCODE
    # Select VSCode type between insiders and normal
    def vscode_type(self, **kwargs) -> dict:

        code_type = kwargs.get("vscode") or inquirer.list_input("", choices=["code", "insiders"])

        code_dir = "code - insiders" if code_type == "insiders" else "code"
        code_PATH = "code-insiders" if code_type == "insiders" else "code"

        vscode = {
            "type": code_PATH,
            "path": code_paths[platform.system()].format(code_dir)
        }

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None

        return vscode

    ##### LANGUAGES
    # Select the most used languages by the user
    def select_languages(self, **kwargs) -> list:

        all_languages = languages.keys()

        selected_languages = self.settings["languages"] or kwargs.get("set_up_languages") or None

        question = inquirer.Checkbox(
            name = "languages",
            message = "Select the languages you use",
            choices = all_languages,
            default = selected_languages)

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None

        return inquirer.prompt([question])["languages"]

    ##### FOLDERS RELATED
    # Get the folders to work on with the workspaces
    def select_folders(self, **kwargs) -> tuple:

        main_dir = kwargs.get("custom_dir") or Path(Path.joinpath(Path.home(), "Documents"))
        create = kwargs.get("create_folders") or inquirer.confirm("", default=False)

        if not os.path.exists(main_dir):
            raise DirectoryNotFound("Specified directory was not found")

        folders = [i.lower() for i in os.listdir(main_dir) if "." not in i]

        if folders and not create:
            sub_directories = self.__select_folders(folders=folders)

        else:
            sub_directories = self.__ask_folders()
            self.__create_folders(
                main_dir=main_dir,
                sub_directories=sub_directories)

        return main_dir, sub_directories

    # Get user selected folders
    def __select_folders(self, folders) -> list:

        if "github" in folders:
            default = ["github"]

        question = inquirer.Checkbox(
            name = "folders",
            message = "Select the folders you want to use",
            choices = folders,
            default = default)

        return inquirer.prompt([question])["folders"]

    # Get folders that user wants to create
    def __ask_folders(self) -> list:

        sub_directories = []

        while True:
            folder = inquirer.text(message="Enter the name for the folder: ")

            if inquirer.confirm(message=f"Want to create a folder called {folder}?"):
                sub_directories.append(folder)

            if not inquirer.confirm(message="Want to add more folders?"):
                return sub_directories

    # Create the new folders
    @yaspin(text=" Creating folders...")
    def __create_folders(self, main_dir: str, sub_directories: list) -> None:

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None

        for i in sub_directories:
            os.mkdir(os.path.join(main_dir, i))

    ##### API KEY
    # Get Api Key and return encrypted version
    def get_api_key(self, **kwargs) -> str:

        new_key = kwargs.get("api_key") or inquirer.text("Introduce la nueva API key.")

        headers = {
            "Authorization": "Bearer " + new_key,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        message = requests.get(url="https://api.github.com/repos/Dtar380/WorkspaceAutomator", headers=headers)

        if message.status_code == 200:
            print("KEY WAS VERIFIED")
        else:
            raise API_KEY_ERROR(f"Failed verificaion [ERROR CODE: {message.status_code}]")

        encrypted_key = Fernet(key_generator(self.key)).encrypt(new_key.encode()).decode()

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            raise Exception("Exiting...")

        return encrypted_key

    ##### GitHub
    # Get GitHub username
    def get_github_username(self, **kwargs) -> str:

        while True:
            username = kwargs.get("github_user") or inquirer.text("Input your GitHub username")

            if inquirer.confirm("") and self.__check_github_user(username=username):
                return username

    def __check_github_user(self, username: str) -> bool:

        if requests.get(f"https://github.com/{username}").status_code != 200:
            print("\nUsername does not exist\n")
            return False

        return True

    ##### SAVE SETTINGS
    # Save the settings to settings.json
    @yaspin(text=" Saving settings...")
    @classmethod
    def save_settings(cls,
        sub_directories: list,
        languages: dict,
        vscode: dict,
        git_username: str,
        api_key: bytes
        ) -> None:

        settings = {
            "folders": sub_directories,
            "languages": languages,
            "vscode": vscode,
            "git-user": git_username
        }

        settings_path = settings_paths[platform.system()]

        with open(SETTINGS, "w+") as f:
            json.dump(settings, f)

        if not os.path.exists(os.path.join(settings_path,)):
            with open(WORKSPACES, "w+") as f:
                pass

        with open(SECRETS, "w+") as f:
            f.write(f'API_KEY = "{api_key.decode()}"')
