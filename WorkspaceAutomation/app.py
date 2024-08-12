########################################
#####  DOCUsystemMENTATION               #####
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

# ENV MANAGEMENT
import subprocess

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
            # NORMAL
            "create": self.__create_workspace,
            "import": self.__import_workspace,
            "delete": self.__delete_workspace,
            "open": self.__open_workspace,
            "publish": self.__publish_workspace,
            "move": self.__move_workspace,
            "edit": self.__edit_workspace,
            # SETTINGS
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
            if directory not in self.settings["directories"]:
                raise DirectoryNotFound("Directory was not found or does not exist.")
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

        if name in os.listdir(directory):
            raise WorkSpaceAlreadyExists("The name is already in use.")

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

            action = 0 if owner == "Dtar380" else 1

            with open("resources/languages.json", "r+") as f:
                data = json.load(f)
                gitignore = data[language]

            Github(
                # PARAMS
                action = action,
                clone = True,
                name = name,
                owner = owner,
                directory = directory,
                # KWARGS
                private = private,
                auto_init = "true",
                gitignore = gitignore,
                license = license
            )

        ContentsManager()

        # ADD A MENU HE RE TO ADD APPS
        apps = self.__select_apps()

        # ADD A MENU HERE TO ADD URLS
        urls = self.__add_urls()
        WebsManager()

        self.__save_workspace(
            directory = directory,
            name = name,
            owner = owner if owner else None,
            private = private if private else None,
            apps = apps,
            urls = urls
        )

    # Import a workspace from your directories in settings.json
    def __import_workspace(self, **kwargs) -> None:
        questions = []

        try:
            name = kwargs["name"]
            directory = kwargs["directory"]
            github = kwargs["github"]
            if directory not in self.settings["directories"]:
                raise DirectoryNotFound("Directory was not found or does not exist.")
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

        if name not in os.listdir(directory):
            raise WorkSpaceNotFound("Workspace was not found with that name")

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

            action = 0 if owner == "Dtar380" else 1

            with open("resources/languages.json", "r+") as f:
                data = json.load(f)
                gitignore = data[language]

            Github(
                # PARAMS
                action = action,
                clone = False,
                name = name,
                owner = owner,
                directory = directory,
                # KWARGS
                private = private,
                auto_init = "true",
                gitignore = gitignore,
                license = license
            )

        # ADD A MENU HE RE TO ADD APPS
        apps = self.__select_apps()

        # ADD A MENU HERE TO ADD URLS
        urls = self.__add_urls()
        WebsManager()

        self.__save_workspace(
            directory = directory,
            name = name,
            owner = owner if owner else None,
            private = private if private else None,
            apps = apps,
            urls = urls
        )

    # Delete a workspace
    def __delete_workspace(self, **kwargs) -> None:

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        try:
            name = kwargs["name"]
        except:
            name = inquirer.text("Enter the name of the project")

        if name not in data.keys():
            raise WorkSpaceNotFound("WorkSpace name was not found or non existing, please try again")

        directory = data[name]["directory"]
        owner = data[name]["owner"]

        del data[name]

        Github(
            action = 2,
            clone = False,
            name = name,
            owner = owner,
            directory = directory
        )

        ContentsManager()

        WebsManager()

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json")):
            json.dump(data, f)

    # Open a workspace
    def __open_workspace(self, **kwargs) -> None:
        
        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        try:
            name = kwargs["name"]
        except:
            name = inquirer.text("Enter the name of the project")

        if name not in data.keys():
            raise WorkSpaceNotFound("WorkSpace name was not found or non existing, please try again")

        directory = data[name]["directory"]

        with open(self.settings["vscode"]["path"]) as f:
            data = json.load(f)

        profiles = []

        for profile in data["userDataProfiles"]:
            profiles.append(profile["name"])

        profile = inquirer.list_input("Select the profile to use", choices=profiles)

        AppsManager()

        WebsManager()

    # Publish a local workspace to a git cloud service
    def __publish_workspace(self, **kwargs) -> None:
        
        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        try:
            name = kwargs["name"]
            owner = kwargs["owner"]
            private = kwargs["private"]
        except:
            questions = [
                inquirer.Text("name", message="Enter the name for the project"),
                inquirer.List("owner", message="Want to create a github repo?", choices=["Yes", "No"]),
                inquirer.List("private", message="Want to make the repo private?", choices=["Yes", "No"] ,default="Yes"),
            ]

            answers = inquirer.prompt(questions)

            name = answers["name"]
            owner = answers["owner"]
            private = "true" if answers["Private"] == "Yes" else "false"

        if name not in data.keys():
            raise WorkSpaceNotFound("Workspace was not found with that name")

        action = 0 if owner == "Dtar380" else 1

        github = Github(
            # PARAMS
            action = action,
            clone = False,
            name = name,
            owner = owner,
            directory = data[name]["directory"],
            # KWARGS
            private = private,
            auto_init = "false",
        )

        github.push_user_repo()

        data[name]["owner"] = owner
        data[name]["private"] = private

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w+") as f:
            data = json.dump(data, f)

    # Move your workspace to another directory
    def __move_workspace(self, **kwargs) -> None:
        pass

    # Edit the selected parameter of your workspace
    def __edit_workspace(self, **kwargs) -> None:
        pass

    # Save the workspace to the json file
    def __save_workspace(self,
            directory: str,
            name: str,
            apps: list,
            urls: list,
            owner: str = None,
            private: str = None
        ) -> None:

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        data[name] = {
            "directory": os.path.join(directory, name),
            "apps": apps,
            "urls": urls,
            "owner": owner,
            "private": private
        }

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w+") as f:
            data = json.dump(data, f)

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

    # SHARED MENUS
    # Selecting apps related
    def __select_apps(self) -> list:
        command_generators = {
            "Windows": self.__find_app_windows,
            "MacOS": self.__find_app_macos,
            "Linux": self.__find_app_linux
        }

        apps = []

        while True:
            app = inquirer.text(message="Enter the name for the App: ")
            
            command = command_generators[self.settings["OS"]](app)

            if command and inquirer.confirm(message=f"Want to use app {app}?"):
                apps.append(command)

            if not inquirer.confirm(message="Want to add more Apps?"):
                return apps

    @yaspin(text=" Finding Application...")
    def __find_app_windows(self, app_name: str) -> list:
        try:
            file = subprocess.run(["powershell.exe", "-c", 'Get-StartApps | Where-Object {{ $_.Name -like "{}" }}'.format(app_name)], capture_output=True)
            app = file.stdout.decode().replace("\r\n","").split(" ")[-1]
            if app:
                return ["powershell.exe", "-c", 'Start-Process Shell:AppsFolder\\{}'.format(app)]
            else:
                print()
                return None
        except:
            print()
            return None

    @yaspin(text=" Finding Application...")
    def __find_app_macos(self, app_name: str):
        try:
            result = subprocess.run(['ls', '/Applications'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            apps = [line for line in result.stdout.splitlines() if app_name.lower() in line.lower()]
            if apps:
                return ['open', f"/Applications/{apps[0]}"]
            else:
                print()
                return None
        except:
            print()
            return None

    @yaspin(text=" Finding Application...")
    def __find_app_linux(self, app_name: str):
        try:
            result = subprocess.run(['which', app_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            app_path = result.stdout.strip()
            if app_path:
                return [app_path]
            else:
                print()
                return None
        except:
            print()
            return None
