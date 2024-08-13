########################################
#####  DOCUMENTATION               #####
########################################

'''
This script manages a system of automatization for the creation, edition, and management of development workspaces.
It allows the creation of GitHub repositories, configuration of environments and administration of APPs and URLs associated with each workspace.
'''

########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# READING APP DATA
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from pathlib import Path
import os
import json

# ENV MANAGEMENT
import subprocess

# URL REQUESTS
from requests import get

#CLI
import inquirer
from yaspin import yaspin

##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# BUILDERS
from .builders.github import Github
from .builders.Contents import ContentsManager

# RUNNERS
from .runners.apps import AppsManager
from .runners.webs import WebsManager

# REUSABLE FUNCTIONS
from .common import key_generator, clear

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from .__vars__ import settings_paths, code_paths

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[os.system()]
os.chdir(MAIN_DIRECTORY)  # Change CWD

########################################
#####  CLASS                       #####
########################################

class App:

    """
    The App class contains all commands that can be executed by user at any moment.
    
    This commands are:
    - Create
    - Import
    - Delete
    - Open
    - Publish
    - Move
    - Edit
    - Config
    """
    
    ##### INITIALISE CLASS
    def __init__(self, command: str, key: str, **kwargs) -> None:

        """
        ## Class Initialization

        Parameters
        ----------
        command: str
            Command to execute.

        key: str
            Password to unlock the API key.

        Raise
        -----
        CommandNotFound: Exception
            Raise if the specified command was not found.
        """

        self.yes = kwargs.get("yes") or False
        self.key = key
        self._load_env_variables()
        self._load_settings()

        commands = {
            # Comandos principales
            "create": self._create_workspace,
            "import": self._import_workspace,
            "delete": self._delete_workspace,
            "open": self._open_workspace,
            "publish": self._publish_workspace,
            "move": self._move_workspace,
            "edit": self._edit_workspace,
            # Comandos de configuración
            "config": {
                "code": self._change_vscode,
                "languages": self._edit_languages,
                "folders": self._edit_folders,
                "api_key": self._change_api_key,
            }
        }

        if command not in commands.keys():
            raise CommandNotFound("The given command was not found")

        # Ejecutar el comando seleccionado
        if command != "config":
            commands[command](**kwargs)
        else:
            commands[command][kwargs["config_type"]](**kwargs)

    def _load_env_variables(self) -> None:

        """
        ## Load Env Settings

        Parameters
        ----------
        key: str
            Encryption key used to decrypt the API key.

        Raises
        -------
        PasswordError: Exception
            Raised if the given password was invalid.
        """

        try:
            load_dotenv(".secrets")
            encrypted_key = os.getenv("API_KEY")
            self.API_KEY = Fernet(key_generator(self.key)).decrypt(encrypted_key).decode()
        except FileNotFoundError:
            raise FileNotFoundError(".secrets file was not found")
        else:
            raise PasswordError("Password is incorrect, API KEY could not get decrypted")

    def _load_settings(self) -> None:

        """
        ## Load Settings

        Raises
        -------
        FileNotFoundError: Exception
            Raised if `settings.json` does not exist.
        """

        if not os.path.exists("settings.json"):
            raise FileNotFoundError("Settings file was not found")

        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    ##### WORKSPACES FUNCTIONS
    def _create_workspace(self, **kwargs) -> None:

        """
        ## Create Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `name`, `directory`, `github`, `owner`, `private`, `license`, etc.

        Raises
        ------
        WorkSpaceAlreadyExists: Exception
            Raised if a workspace with the given name already exists in the specified directory.
        """

        name, directory, github, language = self.__get_workspace_info(**kwargs)
        
        if name in os.listdir(directory):
            raise WorkSpaceAlreadyExists("El nombre ya está en uso.")

        if github:
            owner, private, license = self.__get_github_info(**kwargs)
            
            self.__create_github_repo(
                name=name,
                owner=owner,
                directory=directory,
                language=language,
                private=private,
                license=license,
                clone=False,
                auto_init="true")
            
        apps = self.__select_apps()
        urls = self.__add_urls()

        self.__save_workspace(
            directory=directory,
            name=name,
            apps=apps,
            urls=urls,
            owner=owner,
            private=private)

    def _import_workspace(self, **kwargs) -> None:

        """
        ## Import Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `name`, `directory`, `github`, `owner`, `private`, `license`, etc.

        Raises
        ------
        WorkSpaceNotFound: Exception
            Raised if the workspace with the given name is not found in the specified directory.
        """

        name, directory, github, language = self.__get_workspace_info(**kwargs)

        if name not in os.listdir(directory):
            raise WorkSpaceNotFound("No se encontró el workspace con ese nombre.")

        if github:
            owner, private, license = self.__get_github_info(**kwargs)
            
            self.__create_github_repo(
                name=name,
                owner=owner,
                directory=directory,
                private=private,
                clone=False,
                auto_init="false")

        apps = self.__select_apps()
        urls = self.__add_urls()

        self.__save_workspace(
            directory=directory,
            name=name,
            apps=apps,
            urls=urls,
            owner=owner,
            private=private)

    def _delete_workspace(self, **kwargs) -> None:

        """## Delete Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `name`.

        Raises
        ------
        WorkSpaceNotFound: Exception
            Raised if the workspace with the given name is not found in `workspaces.json`.
        """

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto")
        if name not in data:
            raise WorkSpaceNotFound("No se encontró el workspace con ese nombre.")

        directory = data[name]["directory"]
        owner = data[name]["owner"]

        if not inquirer.confirm(f"Want to delete the workspace {name}?") and not self.yes:
            print("exiting...")
            return None

        del data[name]

        Github(
            action=2,
            clone=False,
            name=name,
            owner=owner,
            directory=directory)
        
        ContentsManager()

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w") as f:
            json.dump(data, f)

    def _open_workspace(self, **kwargs) -> None:

        """
        ## Open Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `name`.

        Raises
        ------
        WorkSpaceNotFound: Exception
            Raised if the workspace with the given name is not found in `workspaces.json`.
        """

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto")
        if name not in data:
            raise WorkSpaceNotFound("No se encontró el workspace con ese nombre.")

        directory = data[name]["directory"]
        profile = self.__select_vscode_profile()

        AppsManager()
        WebsManager()

    def _publish_workspace(self, **kwargs) -> None:

        """
        ## Publish Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `name`, `owner`, `private`, etc.

        Raises
        ------
        WorkSpaceNotFound: Exception
            Raised if the workspace with the given name is not found in `workspaces.json`.
        """

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto")
        owner = kwargs.get("owner") or inquirer.list_input("¿Quién es el propietario del repositorio?")
        private = kwargs.get("private") or "true" if inquirer.confirm("¿El repositorio es privado?", default=False) else "false"

        if name not in data:
            raise WorkSpaceNotFound("No se encontró el workspace con ese nombre.")

        self.__create_github_repo(
            clone=False,
            name=name,
            owner=owner,
            directory=data[name]["directory"],
            private=private,
            auto_init="false",
        )

        data[name]["owner"] = owner
        data[name]["private"] = private

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w") as f:
            json.dump(data, f)

    def _move_workspace(self, **kwargs) -> None:

        """
        ## Move Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `name`, `directory`.

        Raises
        ------
        WorkSpaceNotFound: Exception
            Raised if the workspace with the given name is not found in `workspaces.json`.
        """

        name, new_directory = self.__get_move_workspace_info(**kwargs)

        if not inquirer.confirm(f"Want to move the workspace {name}?") and not self.yes:
            print("Exiting...")
            return None

        ContentsManager()

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        data[name]["directory"] = os.path.join(new_directory, name)

        with open(os.path.join(MAIN_DIRECTORY, "workspace.json"), "w") as f:
            json.dump(data, f)

    def _edit_workspace(self, **kwargs) -> None:

        """
        ## Edit Workspace

        Parameters
        ----------
        kwargs: dict
            Additional parameters such as `add-apps`, `del-apps`, `add-urls`, `del-urls`.

        Raises
        ------
        WorkSpaceNotFound: Exception
            Raised if the workspace with the given name is not found in `workspaces.json`.
        """

        with open(os.path.join(MAIN_DIRECTORY, "workspace.json"), "r+") as f:
            data = json.load(f)

        if kwargs.get("add-apps"):
            apps = self.__select_apps()
            data["apps"] += apps
        if kwargs.get("del-apps"):
            apps_to_delete = inquirer.Checkbox("apps", message="Selecciona las aplicaciones a eliminar.", choices=data["apps"].keys())
            for app in inquirer.prompt([apps_to_delete])["apps"]:
                del data["apps"][app]

        if kwargs.get("add-urls"):
            urls = self.__add_urls()
            data["urls"].extend(urls)
        if kwargs.get("del-urls"):
            urls_to_delete = inquirer.Checkbox("urls", message="Selecciona las URLs a eliminar.", choices=data["urls"])
            for url in inquirer.prompt([urls_to_delete])["urls"]:
                data["urls"].remove(url)

        if not inquirer.confirm("Want to perform changes?") and not self.yes:
            print("Exiting...")
            return None
        
        with open(os.path.join(MAIN_DIRECTORY, "workspace.json"), "r+") as f:
            data = json.dump(data, f)

    def __save_workspace(self,
        directory: str,
        name: str,
        apps: list,
        urls: list,
        owner: str = None,
        private: str = None
        ) -> None:

        """
        ## Save Workspace

        Parameters
        ----------
        directory: str
            The directory where the workspace is stored.

        name: str
            The name of the workspace.

        apps: list
            A list of applications associated with the workspace.

        urls: list
            A list of URLs associated with the workspace.

        owner: str, optional
            The owner of the GitHub repository.

        private: str, optional
            Indicates if the GitHub repository is private.
        """

        if not inquirer.confirm("Want to create the WorkSpace?") and not self.yes:
            print("Exiting...")
            return None

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        data[name] = {
            "directory": os.path.join(directory, name),
            "apps": apps,
            "urls": urls,
            "owner": owner,
            "private": private
        }

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w") as f:
            json.dump(data, f)

    ##### CONFIG FUNCTIONS
    @yaspin(text="Guardando cambios...")
    def _change_vscode(self, **kwargs) -> None:

        """
        ## Change VsCode

        Parameters
        ----------
        kwargs: dict
            Uses `vscode-type` (e.g. `code` or `insiders`).
        """

        code_dir = "code - insiders" if kwargs["vscode-type"] == "insiders" else "code"
        code_PATH = "code-insiders" if kwargs["vscode-type"] == "insiders" else "code"
        
        self.settings["vscode"] = {
            "type": code_PATH,
            "path": code_paths[os.system()].format(code_dir)
        }

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None
        
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def _edit_languages(self, **kwargs) -> None:

        """
        ## Edit Languages
        """

        with open("resources/languages.json", "r+") as f:
            all_languages = json.load(f).keys()

        question = inquirer.Checkbox(
            name = "languages",
            message = "Select the languages you use",
            choices = all_languages,
            default = self.settings["langauges"])
        languages = inquirer.prompt([question])["languages"]
        self.settings["languages"] = languages

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None

        with open("settings.json", "w+") as f:
            json.dump(self.settings, f)

    def _edit_folders(self, **kwargs) -> None:

        """
        ## Edit Folders

        Parameters
        ----------
        kwargs: dict
            Uses `main-directory`.
        """

        main_dir = kwargs["main-directory"] or Path(Path.joinpath(Path.home(), "Documents"))

        folders = [i.lower() for i in os.listdir(main_dir) if "." not in i]
        if folders and not inquirer.confirm("Want to create folders"):
            sub_directories = self.__select_folders(folders)
        else:
            sub_directories = self.__ask_folders()
            self.__create_folders(main_dir, sub_directories)
        
        self.settings["directories"] = sub_directories

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None
        
        with open("settings.json", "w+") as f:
            json.dump(self.settings, f)

    def __select_folders(self, folders: list) -> list:

        if "github" in folders:
            default = ["github"]

        question = inquirer.Checkbox(
            name = "folders", 
            message = "Select the folders you want to use",
            choices = folders,
            default = default)
        
        return inquirer.prompt([question])["folders"]

    def __ask_folders(self) -> None:

        sub_directories = []

        while True:
            folder = inquirer.text(message="Enter the name for the folder: ")
            if inquirer.confirm(message=f"Want to create a folder called {folder}?"):
                sub_directories.append(folder)
            if not inquirer.confirm(message="Want to add more folders?"):
                return sub_directories

    @yaspin(text=" Creating the folders...")
    def __create_folders(self,
        main_dir: str,
        sub_directories: list) -> None:

        for i in sub_directories: 
            os.mkdir(os.path.join(main_dir, i))

    def _change_api_key(self, **kwargs) -> None:

        """
        ## Change API KEY

        Parameters
        ----------
        kwargs: dict
            Uses `key`.
        """

        new_key = kwargs.get("key") or inquirer.text("Introduce la nueva API key.")

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
        
        encrypted_key = Fernet(key_generator(self.key)).encrypt(new_key.encode()).decode()

        if not inquirer.confirm("Want to save changes?") and not self.yes:
            print("Exiting...")
            return None

        with open(".secrets", "w") as f:
            f.write(f'API_KEY = "{encrypted_key}"\n')

    ##### SHARED MENUS
    # Select Apps to boot when opening a WorkSpace
    def __select_apps(self) -> dict:

        """
        ## Select Apps

        Returns
        -------
        dict: dict
            A dictionary of selected applications and their launch commands.
        """

        command_generators = {
            "Windows": self.__find_app_windows,
            "MacOS": self.__find_app_macos,
            "Linux": self.__find_app_linux
        }

        apps = {}

        while True:
            app = inquirer.text(message="Enter the name for the App: ")
            
            command = command_generators[self.settings["OS"]](app)

            if not command:
                print(f"{app} Was not found")
            elif inquirer.confirm(message=f"Want to use app {app}?"):
                apps[app] = command

            if not inquirer.confirm(message="Want to add more Apps?"):
                return apps

    # FIND APPS IN EACH OS
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

    # Add urls to a WorkSpace
    def __add_urls(self) -> list:
        
        """
        ## Add Urls

        Returns
        -------
        list: list
            A list of URLs added by the user.
        """

        urls = []
        while True:
            url = inquirer.text("Enter a url")
            
            if get(url).status_code != 200:
                print(f"{url} was unable to fetch")
            elif inquirer.confirm(message=f"Want to add url {url}?"):
                urls.append(url)

            if not inquirer.confirm(message="Want to add more Apps?"):
                return urls

    # Get information to create workspace
    def __get_workspace_info(self, **kwargs) -> tuple:
        
        """
        ## Get Workspace Info

        Parameters
        ----------
        kwargs: dict
            Takes the positional parameters of:
            `Name`, name for the workspace.
            `Directory`, directory for the workspace.
            `GitHub`, flare for using github.
            `Language`, language used for the workspace.
        """

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto:")
        directory = kwargs.get("directory") or inquirer.list_input("Selecciona la carpeta del proyecto:", choices=self.settings["directories"])
        github = kwargs.get("github") or inquirer.confirm("¿Deseas crear un repositorio de GitHub?", default=True)
        language = kwargs.get("language") or inquirer.list_input("Selecciona el lenguaje de programación principal:", choices=self.settings["languages"])

        return name, directory, github, language

    # Get information to create github repo
    def __get_github_info(self, get_license: bool, **kwargs) -> tuple:
        
        """
        ## Get GitHub Info

        Parameters
        ----------
        kwargs: dict
            Takes the positional parameters of:
            `owner`, owner of the repo.
            `private`, flag to make repo private.
            `license`, license of the repo
        """

        owner = kwargs.get("owner") or inquirer.text("Introduce el propietario del repositorio:")
        private = kwargs.get("private") or "true" if inquirer.confirm("¿El repositorio es privado?", default=False) else "false"
        if get_license:
            license = kwargs.get("license") or inquirer.list_input("Introduce la licencia:", choices=["MIT", "GPL-3.0", "Unlicense"])
        else:
            license = None

        return owner, private, license

    # Create a github repo and create initial commit
    def __create_github_repo(self,
        name: str,
        owner: str,
        directory: str,
        private: str,
        clone: bool,
        auto_init: str,
        license: str = None,
        language: str = None
        ) -> None:
        
        """
        ## Create GitHub Repo

        Parameters
        ----------
        name: str
            Name of the repo

        owner: str
            Owner of the repo

        directory: str
            Directory of the workspace

        private: str
            Privacy type for the repo

        clone: bool
            Clone or not the repo

        auto_init: str
            Auto initiate the repo with README, LICENSE and .gitignore
        
        license: str, optional
            License for the repo

        language: str, optional
            Language used in the repo
        """

        if not inquirer.confirm("Want to create the repo?") and not self.yes:
            print("Exiting...")
            return None
        
        action = 0 if owner == self.settings["git-user"] else 1

        github = Github(
            action=action,
            clone=clone,
            name=name,
            owner=owner,
            directory=directory,
            private=private,
            auto_init=auto_init,
            license=license,
            language=language
        )

        github.push_user_repo()

    # Select VSCode profile to open WorkSpace with
    def __select_vscode_profile(self) -> str:
        
        """
        ## Select VSCode Profile

        Returns
        -------
        profile: str
            VSCode profile
        """

        with open(self.settings["vscode"]["path"]) as f:
            profiles = json.load(f)["userDataProfiles"]

        profile_names = [profile["name"] for profile in profiles]

        profiles = inquirer.Checkbox(
            "profiles",
            message="Selecciona el perfil de VSCode:",
            choices=profile_names
        )

        return inquirer.prompt([profiles])["profiles"]

    # Get information about which and where to move a WorkSpace
    def __get_move_workspace_info(self, **kwargs) -> tuple:
        
        """
        ## Get Move Workspace Info

        Parameters
        ----------
        kwargs: dict
            Takes the positional parameters of:
            `Name`, Name of the workspace.
            `New Directory`, New directory to move in workspace.

        Returns
        -------
        name: str
            Name of the workspace.

        new_directory: str
            `New Directory`, New directory to move in workspace.
        """

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto:")
        new_directory = kwargs.get("new_directory") or inquirer.list_input("Selecciona la nueva carpeta del proyecto:", choices=self.settings["folders"])

        return name, new_directory
