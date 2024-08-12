########################################
#####  DOCUMENTATION               #####
########################################

'''

'''

########################################
#####  IMPORTING MODULES           #####
########################################

# FILE MANAGEMENT
from os import mkdir
from cryptography.fernet import Fernet
from .common import key_generator
import json

# ENV MANAGEMENT
from pathlib import Path
from platform import system
import subprocess
from os import path, listdir

# API CHECKER
from requests import get

# CLI
import inquirer
from yaspin import yaspin
from .common import clear

########################################
#####  CODE                        #####
########################################

##### GLOBAL VARIABLES
from .__vars__ import settings_paths, code_paths

#####  CLASS
class SetUp:

    def __init__(self, custom_directory: str = None) -> None:

        clear(0)
        if not path.exists(settings_paths[system()]):
            mkdir(settings_paths[system()])
            self.OS = self.__check_compatibility()
        clear(0.5)

        self.key = key_generator(inquirer.text(message="Enter a password (this will be used to encrypt the API_KEY)"))

        if custom_directory:
            self.directory = custom_directory
        else:
            self.directory = Path(Path.joinpath(Path.home(), "Documents"))
        
        self.folders = self.__get_folders()

        if self.folders and not inquirer.confirm(message="Want to create folders?"):
            self.sub_directories = self.__select_folders()
        else:
            self.sub_directories = self.__ask_folders()
            self.__create_folders()

        clear(0.5)

        with open("resources/languages.json", "r+") as f:
            self.languages = json.load(f).keys()

        self.username = self.__get_github_username()
        clear(0.5)
        self.languages = self.__select_languages()
        clear(0.5)
        self.vscode = inquirer.list_input(message="What version of VSCode do you use", choices=["code", "insiders"])
        clear(0.5)
        self.API_KEY = self.__get_api_key()
        clear(0.5)

        self.__save_settings()
        clear(0.5)
        exit()

    # CHECK IF OS IS COMPATIBLE
    @yaspin(text=" Checking compatibility...")
    def __check_compatibility(self) -> str:
        if system() == "Linux":
            return "Linux"
        elif system() == "Darwin":
            return "MacOS"
        elif system() == "Windows":
            return "Windows"
        else:
            raise Exception("Not compatible Operating System")

    # FUNCTIONS RELATED WITH PATHS FOR THE APP
    @yaspin(text=" Listing folders in Documents...")
    def __get_folders(self) -> list:
        return [i.lower() for i in listdir(self.directory) if "." not in i]

    def __select_folders(self) -> list:

        if "github" in self.folders:
            default = ["github"]

        question = [inquirer.Checkbox(
            name = "folders", 
            message = "Select the folders you want to use",
            choices = self.folders,
            default = default)]
        
        answer = inquirer.prompt(question)
        return answer["folders"]

    def __ask_folders(self) -> list:
        folders = []

        while True:
            folder = inquirer.text(message="Enter the name for the folder: ")
            if inquirer.confirm(message=f"Want to create a folder called {folder}?"):
                folders.append(folder)
            if not inquirer.confirm(message="Want to add more folders?"):
                return folders

    @yaspin(text=" Creating the folders...")
    def __create_folders(self) -> None:
        for i in self.sub_directories:
            mkdir(path.join(self.directory, i))

    # FUNCTIONS FOR GETTING GH USERNAME
    def __get_github_username(self) -> str:
        while True:
            user_name = inquirer.text(message="Enter your GitHub username")
            response = get(f"https://github.com/{user_name}")
            if response.status_code != 200:
                print(f"User {user_name} was not found. Please try again")
            else:
                return user_name

    # FUNCTION FOR SELECTING LANGS USED BY USER
    def __select_languages(self) -> list:
        question = [inquirer.Checkbox(
            name = "languages",
            message = "Select the languages you use",
            choices = self.languages)]
    
        answer = inquirer.prompt(question)
        return answer["languages"]

    # FUNCTIONS RELATED WITH APP SELECTION
    

    # GET USER INPUT API KEY AND CHECK IF ITS VALID
    def __get_api_key(self) -> str:
        while True:
            key = inquirer.text(message="Input you GitHub API Key")
            
            headers = {
                "Authorization": "Bearer " + key,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }

            response = get(url="https://api.github.com/repos/Dtar380/WorkspaceAutomator", headers=headers)
            
            if response.status_code == 200:
                print("KEY WAS VERIFIED")
                return key
            else:
                print(f"An error occurred please retry (ERROR CODE: {response.status_code})\n\n")

    # SAVE SETTINGS TO THE SETTINGS FILE
    @yaspin(text=" Saving settings...")
    def __save_settings(self) -> None:

        code_dir = "code - insiders" if self.vscode == "insiders" else self.vscode
        code_PATH = "code-insiders" if self.vscode == "insiders" else self.vscode

        code_path = code_paths[system()].format(code_dir)

        settings = {
            "directories": self.sub_directories,
            "languages": self.languages,
            "vscode": {
                "type": code_PATH,
                "path": code_path
            },
            "git-user": self.username,
            "OS": self.OS
        }

        settings_path = settings_paths[system()]

        with open(path.join(settings_path, "settings.json"), "w+") as f:
            json.dump(settings, f)

        if not path.exists(path.join(settings_path, "workspaces.json")):
            with open(path.join(settings_path, "workspaces.json", "w+")) as f:
                pass

        self.API_KEY = Fernet(self.key).encrypt(self.API_KEY.encode())

        with open(path.join(settings_path, ".secrets"), "w+") as f:
            f.write(f'API_KEY = "{self.API_KEY}"')
