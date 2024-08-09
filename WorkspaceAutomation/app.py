########################################
#####  DOCUMENTATION               #####
########################################

'''

'''

########################################
#####  IMPORTING MODULES           #####
########################################

# READING APP DATA
from dotenv import load_dotenv
from pathlib import Path
import os
import json

# API CHECKER
from requests import get

# CLI
import inquirer
from yaspin import yaspin
from .common import clear

# ERRORS
from .__errors__ import *

########################################
#####  CODE                        #####
########################################

##### GLOBAL VARIABLES    
settings_paths = {
    "Windows": str(Path.home()) + f"\\AppData\\Roaming\\WorkSpaceAutomation",
    "Darwin": str(Path.home()) + f"\\Library\\Application\\ Support\\WorkSpaceAutomation",
    "Linux": str(Path.home()) + f"\\.config\\WorkSpaceAutomation"
}

# MOVE TO SETTINGS PATH
MAIN_DIRECTORY = settings_paths[os.system()]
os.chdir(MAIN_DIRECTORY) # CWD

#####  CLASS
class App:

    def __init__(self, command: str, **kwargs) -> None:
        
        # DICT CONTAINING ALL COMMANDS AVIABLE
        commands = {
            "create": self.__create_workspace,
            "import": self.__import_workspace,
            "delete": self.__delete_workspace,
            "open": self.__open_workspace,
            "publish": self.__publish_workspace,
            "move": self.__move_workspace,
            "edit": self.__edit_workspace,
            "config": {
                "code": self.__change_vscode,
                "languages": self.__edit_languages,
                "folders": self.__edit_folders,
                "api_key": self.__change_api_key,
            }
        }

        # LOAD API_KEY
        load_dotenv(".secrets")
        self.API_TOKEN = os.getenv("API_KEY")

        # LOAD SETTINGS
        with open("settings.json", "r+") as f:
            self.settings = json.load(f)

        # EXECUTE SELECTED COMMAND
        if command != "config":
            commands[command](kwargs)
        else:
            commands[command][kwargs["config_type"]](kwargs)

    # WORKSPACE RELATED
    # Create a new workspace from scratch
    def __create_workspace(self, **kwargs) -> None:
        pass

    # Import a workspace from your directories in settings.json
    def __import_workspace(self, **kwargs) -> None:
        pass

    # Delete a workspace
    def __delete_workspace(self, **kwargs) -> None:
        pass

    # Open a workspace
    def __open_workspace(self, **kwargs) -> None:
        pass
    
    # Publish a local workspace to a git cloud service
    def __publish_workspace(self, **kwargs) -> None:
        pass

    # Move your workspace to another directory
    def __move_workspace(self, **kwargs) -> None:
        pass

    # Edit the selected parameter of your workspace
    def __edit_workspace(self, **kwargs) -> None:
        pass

    # CONFIG RELATED
    # Change VsCode paths in settings.json
    @yaspin(text=" Saving changes...")
    def __change_vscode(self, **kwargs) -> None:
        if kwargs["vscode-type"] == "code":
            code_dir = "code"
            code_PATH = "code"
        elif kwargs["vscode-type"] == "insiders":
            code_dir = "code - insiders"
            code_PATH = "code-insiders"

        code_paths = {
            "Windows": str(Path.home()) + f"\\AppData\\Roaming\\{code_dir}\\User\\globalStorage\\storage.json",
            "Darwin": str(Path.home()) + f"\\Library\\Application\\ Support\\{code_dir}\\User\\globalStorage\\storage.json",
            "Linux": str(Path.home()) + f"\\.config\\{code_dir}\\User\\globalStorage\\storage.json"
        }

        self.settings["vscode"] = {
            "type": code_PATH,
            "path": code_paths[os.system()]
        }

        with open("settings.json", "w+") as f:
            json.dump(self.settings, f)

    # Editing languages from settings.json
    def __edit_languages(self, **kwargs) -> None:
        with open("resources/languages.json", "r+") as f:
            langauges = json.load(f).keys()

        question = [inquirer.Checkbox(
            name = "languages",
            message = "Select the languages you use",
            choices = langauges,
            default = self.settings["langauges"])]
    
        answer = inquirer.prompt(question)
        self.settings["languages"] = answer["languages"]

        with open("settings.json", "w+") as f:
            json.dump(self.settings, f)

    # Editing folders from settings.json
    def __edit_folders(self, **kwargs) -> None:
        if kwargs["main-directory"]:
            main_dir: str = kwargs["main-directory"]
        else:
            main_dir = Path(Path.joinpath(Path.home(), "Documents"))
        
        folders = [i.lower() for i in os.listdir(main_dir) if "." not in i]

        if folders and not inquirer.confirm(message="Want to create folders?"):
            sub_directories = self.__select_folders(folders)
        else:
            sub_directories = self.__ask_folders()
            self.__create_folders(main_dir, sub_directories)

    def __select_folders(self, folders: list) -> list:
        if "github" in folders:
            default = ["github"]

        question = [inquirer.Checkbox(
            name = "folders", 
            message = "Select the folders you want to use",
            choices = folders,
            default = default)]
        
        answer = inquirer.prompt(question)
        sub_directories = answer["folders"]

    def __ask_folders(self) -> None:
        sub_directories = []

        while True:
            folder = inquirer.text(message="Enter the name for the folder: ")
            if inquirer.confirm(message=f"Want to create a folder called {folder}?"):
                sub_directories.append(folder)
            if not inquirer.confirm(message="Want to add more folders?"):
                return sub_directories

    @yaspin(text=" Creating the folders...")
    def __create_folders(self, main_dir, sub_directories) -> None:
        for i in sub_directories: 
            os.mkdir(os.path.join(main_dir, i))

    # Editing API_KEY on .secrets
    @yaspin(text=" Saving changes...")
    def __change_api_key(self, **kwargs) -> None:
        new_key = kwargs["API-KEY"]

        headers = {
            "Authorization": "Bearer " + new_key,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        message = get(url="https://api.github.com/repos/Dtar380/WorkspaceAutomator", headers=headers)

        if message.status_code == 200:
            print("KEY WAS VERIFIED")
        else:
            raise API_KEY_ERROR(f"Failed verificaion [ERROR CODE: {message.status_code}]")
        
        with open(".secrets", "w+") as f:
            f.write(f'API_KEY = "{new_key}"')
