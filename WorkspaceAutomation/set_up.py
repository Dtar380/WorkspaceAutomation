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

#####  CLASS
class SetUp:
        
    settings_paths = {
        "Windows": str(Path.home()) + f"\\AppData\\Roaming\\WorkSpaceAutomation",
        "Darwin": str(Path.home()) + f"\\Library\\Application\\ Support\\WorkSpaceAutomation",
        "Linux": str(Path.home()) + f"\\.config\\WorkSpaceAutomation"
    }

    def __init__(self, custom_directory: str = None) -> None:

        clear(0)
        if not path.exists(self.settings_paths[system()]):
        self.OS = self.__check_compatibility()
        clear(0.5)

        if custom_directory:
            self.directory = custom_directory
            self.folders = self.__get_folders()
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
    def __check_compatibility(self) -> None:
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

        git_services = ["git", "github", "gitlab"]
        for git_service in git_services:
            if git_service in self.folders:
                default = [git_service]

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

    # FUNCTION FOR SELECTING LANGS USED BY USER
    def __select_languages(self) -> list:
        question = [inquirer.Checkbox(
            name = "languages",
            message = "Select the languages you use",
            choices = self.languages)]
    
        answer = inquirer.prompt(question)
        return answer["languages"]

    # FUNCTIONS RELATED WITH APP SELECTION
    def __select_apps(self) -> list:
        apps = []

        while True:
            app = inquirer.text(message="Enter the name for the App: ")
            
            command: bool = False

            if command and inquirer.confirm(message=f"Want to use app {app}?"):
                apps.append(app)

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

    # GET USER INPUT API KEY AND CHECK IF ITS VALID
    def __get_api_key(self) -> None:
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

        code_paths = {
            "Windows": str(Path.home()) + f"\\AppData\\Roaming\\{code_dir}\\User\\globalStorage\\storage.json",
            "Darwin": str(Path.home()) + f"\\Library\\Application\\ Support\\{code_dir}\\User\\globalStorage\\storage.json",
            "Linux": str(Path.home()) + f"\\.config\\{code_dir}\\User\\globalStorage\\storage.json"
        }

        code_path = code_paths[system()]

        settings = {
            "directories": self.sub_directories,
            "languages": self.languages,
            "vscode": {
                "type": code_PATH,
                "path": code_path
            },
            "OS": self.OS
        }

        settings_path = self.settings_paths[system()]

        mkdir(settings_path)

        with open(path.join(settings_path, "settings.json"), "w+") as f:
            json.dump(settings, f)

        with open(path.join(settings_path, ".secrets"), "w+") as f:
            f.write(f'API_KEY = "{self.API_KEY}"')
