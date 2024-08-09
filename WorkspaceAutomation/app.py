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

        if command != "config":
            commands[command](kwargs)
        else:
            commands[command][kwargs["config_type"]](kwargs)

    # WORKSPACE RELATED
    def __create_workspace(self, **kwargs) -> None:
        pass

    def __import_workspace(self, **kwargs) -> None:
        pass

    def __delete_workspace(self, **kwargs) -> None:
        pass

    def __open_workspace(self, **kwargs) -> None:
        pass
    
    def __publish_workspace(self, **kwargs) -> None:
        pass

    def __move_workspace(self, **kwargs) -> None:
        pass

    def __edit_workspace(self, **kwargs) -> None:
        pass

    # CONFIG RELATED
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

    def __edit_folders(self, **kwargs) -> None:
        pass

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

#####  RUN FILE
if __name__ == "__main__":
    pass