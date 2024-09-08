########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# READING APP DATA
import json

# ENV MANAGEMENT
import subprocess
import os
import platform

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

        name = kwargs.get("name") or inquirer.text("Enter the name of your WorkSpace")
        directory = kwargs.get("directory") or inquirer.list_input("Select the directory for your WorkSpace", choices=directories)
        github = kwargs.get("github") or inquirer.confirm("Do you want to create a GitHub repository?", default=True)

        if get_language:
            language = kwargs.get("language") or inquirer.list_input("Select the main language for the project", choices=languages)
        else:
            language = None

        return name, directory, github, language

    # Get info to create GitHub repo
    @classmethod
    def get_github_info(cls, default_owner: str, get_license: bool, **kwargs) -> tuple:

        owner = kwargs.get("owner") or inquirer.text("Enter the name of the owner of the repository", default=default_owner)
        private = kwargs.get("private") or "true" if inquirer.confirm("Do you want to create a private repository?", default=False) else "false"

        if get_license:
            license = kwargs.get("license") or inquirer.list_input("Enter a license", choices=["MIT", "GPL-3.0", "Unlicense"])
        else:
            license = None

        return owner, private, license

    # Get ingo to move a WorkSpace to another Path
    @classmethod
    def get_move_workspace_info(cls, directories: list, **kwargs) -> tuple:

        name = kwargs.get("name") or inquirer.text("Enter the name of your WorkSpace")
        new_directory = kwargs.get("new_directory") or inquirer.list_input("Select the new directory for the WorkSpace", choices=directories)

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
            
            app = inquirer.text(message="Enter the name of the APP")

            command = command_generators[platform.system()](app)

            if not command:
                print(f"The App '{app}' Was not found")
            elif inquirer.confirm(message=f"Want to use the APP {app}"):
                apps[app] = command

            if not inquirer.confirm(message="Want to add more APPs?"):
                return apps

    # Find APPs in each supported OS
    # Find app pn Windows
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

    # Find app on macOS
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

    # Find app on Linux
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

        with open(vscode_settings, "r+") as f:
            profiles = json.load(f)["userDataProfiles"]

        profile_names = [profile["name"] for profile in profiles]

        profiles = inquirer.Checkbox(
            "profiles",
            message="Selecciona el perfil de VSCode:",
            choices=profile_names
        )

        return inquirer.prompt([profiles])["profiles"]
