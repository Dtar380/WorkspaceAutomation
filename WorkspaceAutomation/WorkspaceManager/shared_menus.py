########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# READING APP DATA
import json

# ENV MANAGEMENT
import subprocess
import os

# URL REQUESTS
import requests

# CLI
import inquirer
from yaspin import yaspin

##### INTERNAL IMPORTS
# ERRORS
from ..__errors__ import *

########################################
#####  CLASS                       #####
########################################

class SharedMenus:

    # GET INFO
    # Get info to create a WorkSpace
    @classmethod
    def get_workspace_info(cls, directories: list, languages: list, get_language: bool, **kwargs) -> tuple:

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto:")
        directory = kwargs.get("directory") or inquirer.list_input("Selecciona la carpeta del proyecto:", choices=directories)
        github = kwargs.get("github") or inquirer.confirm("¿Deseas crear un repositorio de GitHub?", default=True)

        if get_language:
            language = kwargs.get("language") or inquirer.list_input("Selecciona el lenguaje de programación principal:", choices=languages)
        else:
            language = None

        return name, directory, github, language

    # Get info to create GitHub repo
    @classmethod
    def get_github_info(cls, get_license: bool, **kwargs) -> tuple:

        owner = kwargs.get("owner") or inquirer.text("Introduce el propietario del repositorio:")
        private = kwargs.get("private") or "true" if inquirer.confirm("¿El repositorio es privado?", default=False) else "false"
         
        if get_license:
            license = kwargs.get("license") or inquirer.list_input("Introduce la licencia:", choices=["MIT", "GPL-3.0", "Unlicense"])
        else:
            license = None

        return owner, private, license

    # Get ingo to move a WorkSpace to another Path
    @classmethod
    def get_move_workspace_info(cls, directories: list, **kwargs) -> tuple:

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto:")
        new_directory = kwargs.get("new_directory") or inquirer.list_input("Selecciona la nueva carpeta del proyecto:", choices=directories)

        return name, new_directory

    # SELECTION MENUS
    # Select APPs to boot when opening a WorkSpace
    @classmethod
    def select_apps(cls) -> dict:

        command_generators = {
            "Windows": cls.__find_app_windows,
            "Darwin": cls.__find_app_macos,
            "Linux": cls.__find_app_linux
        }

        apps = {}

        while True:
            app = inquirer.text(message="Enter the name for the App:")

            command = command_generators[os.system()](app)

            if not command:
                print(f"The App '{app}' Was not found")
            elif inquirer.confirm(message=f"Want to use the app {app}"):
                apps[app] = command

            if not inquirer.confirm(message="Want to add more APPs?"):
                return apps

    # Find APPs in each supported OS
    @yaspin(text=" Finding Application...")
    def __find_app_windows(self, app_name: str) -> list:
        
        try:
            file = subprocess.run(["powershell.exe", "-c", 'Get-StartApps | Where-Object {{ $_.Name -like "{}" }}'.format(app_name)], capture_output=True)
            app = file.stdout.decode().replace("\r\n","").split(" ")[-1]
            
            if app:
                return ["powershell.exe", "-c", 'Start-Process Shell:AppsFolder\\{}'.format(app)]
            else:
                return None
        
        except:
            return None

    @yaspin(text=" Finding Application...")
    def __find_app_macos(self, app_name: str):
        
        try:
            result = subprocess.run(['ls', '/Applications'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            apps = [line for line in result.stdout.splitlines() if app_name.lower() in line.lower()]
            
            if apps:
                return ['open', f"/Applications/{apps[0]}"]
            else:
                return None
            
        except:
            return None

    @yaspin(text=" Finding Application...")
    def __find_app_linux(self, app_name: str):
        
        try:
            result = subprocess.run(['which', app_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            app_path = result.stdout.strip()
            
            if app_path:
                return [app_path]
            else:
                return None
            
        except:
            return None

    # Select URLs to open when opening a WorkSpace
    @classmethod
    def select_urls(cls) -> list:

        urls = []

        while True:
            url = inquirer.text("Enter a URL")

            if requests.get(url).status_code != 200:
                print(f"{url} was unable to fetch")
            elif inquirer.confirm(message=f"Want to add the URL {url}"):
                urls.append(url)

            if not inquirer.confirm(message="Want to add more URLs"):
                return urls

    # GET OPENING INFO
    # Get VSCode profile to open with the WorkSpace
    @classmethod
    def select_vscode_profile(cls, vscode_settings: str) -> str:

        with open(vscode_settings) as f:
            profiles = json.load(f)["userDataProfiles"]

        profile_names = [profile["name"] for profile in profiles]

        profiles = inquirer.Checkbox(
            "profiles",
            message="Selecciona el perfil de VSCode:",
            choices=profile_names
        )

        return inquirer.prompt([profiles])["profiles"]
