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
from cryptography.fernet import Fernet
from .common import key_generator
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

# INTERNAL IMPORTS
from builders.github import Github
from builders.Contents import ContentsManager
from runners.apps import AppsManager
from runners.webs import WebsManager

########################################
#####  CODE                        #####
########################################

##### GLOBAL VARIABLES
from .__vars__ import settings_paths, code_paths

# MOVE TO SETTINGS PATH
MAIN_DIRECTORY = settings_paths[os.system()]
os.chdir(MAIN_DIRECTORY) # CWD

#####  CLASS
class App:

    def __init__(self, command: str, key: str, **kwargs) -> None:

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
        self.API_KEY = os.getenv("API_KEY")
        self.API_KEY = Fernet(key_generator(key)).decrypt(self.API_KEY).decode()

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

        questions = []

        try:
            name = kwargs["name"]
            directory = kwargs["directory"]
            github = kwargs["github"]
        except:
            questions.extend([
                inquirer.List("directory", message="Select the directory for the project", choices=self.settings["directories"]),
                inquirer.Text("name", message="Enter the name for the project"),
                inquirer.List("github", message="Want to create a github repo?", choices=["Yes", "No"])
            ])

        questions.append(inquirer.List("langauge",message = "What will be the main language", choices=self.settings["langauges"]))

        answers = inquirer.prompt(questions)
        language = answers["language"]

        try:
            name = answers["name"]
            directory = answers["directory"]
            github = True if answers["github"] == "Yes" else False
        except:
            pass

        questions = []

        if github:
            try:
                owner = kwargs["owner"]
                private = kwargs["private"]
                license = kwargs["license"]
                if license and license not in ["MIT", "GPL-3.0", "Unlicense"]:
                    raise LicenseNotFound("License provided is not supported.")
            except:
                questions.extend([
                    inquirer.Text("owner", message="Enter the owner of the Repo: ", default=self.settings["git-user"]),
                    inquirer.List("private", message="Want to make the repo private?", choices=["Yes", "No"] ,default="Yes"),
                    inquirer.List("license", message="What license do you want to use?", choices=["MIT", "GPL-3.0", "Unlicense"])
                ])

                answers = inquirer.prompt(questions)
                owner = answers["owner"]
                private = "true" if answers["private"] == "Yes" else "false"
                license = answers["license"]

            if owner == self.settings["git-user"]:
                action = 0
            else:
                action = 1

            with open("resources/languages.json", "r+") as f:
                data = json.load(f)
                language = data[language]

            Github()

        ContentsManager()

        # ADD A MENU HERE TO ADD APPS
        AppsManager()

        # ADD A MENU HERE TO ADD URLS
        WebsManager()

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

    # Save urls on the go with this command
    def __save_urls(self, **kwargs) -> None:
        pass

    # Save the workspace to the json file
    def __save_workspace(self, **kwargs) -> None:
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

        self.settings["vscode"] = {
            "type": code_PATH,
            "path": code_paths[os.system()].format(code_dir)
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
