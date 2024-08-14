########################################
#####  IMPORTING MODULES           #####
########################################

##### EXTERNAL IMPORTS
# READING APP DATA
import json

# ENV MANAGEMENT
import os

# CLI
import inquirer
from yaspin import yaspin

##### INTERNAL IMPORTS
# ERRORS
from ..__errors__ import *

# CLI
from shared_menus import SharedMenus

# BUILDERS
from .builders.github import Github
from .builders.Contents import ContentsManager

# RUNNERS
from .runners.apps import AppsManager
from .runners.webs import WebsManager

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from ..__vars__ import settings_paths

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[os.system()]

########################################
#####  CLASS                       #####
########################################

class WorkspaceFunctions:

    ##### INITIALISE CLASS
    def __init__(self,
        command: str,
        api_key: str,
        settings: dict,
        yes: bool = False,
        **kwargs
        ) -> None:

        self.api_key = api_key
        self.settings = settings
        self.yes = yes

        commands = {
            "create": self.create_workspace,
            "import": self.import_workspace,
            "delete": self.delete_workspace,
            "open": self.open_workspace,
            "publish": self.publish_workspace,
            "move": self.move_workspace,
            "edit": self.edit_workspace,
        }

        commands[command](**kwargs)

    ##### WORKSPACE FUNCTIONS
    # Create a new WorkSpace
    def create_workspace(self, **kwargs) -> None:

        name, directory, github, language = SharedMenus.get_workspace_info(
            directories=self.settings["folders"],
            languages=self.settings["languages"].keys(),
            get_language=True,
            kwargs=kwargs
        )

        if name in os.listdir(directory):
            raise WorkSpaceAlreadyExists("This name is already being used")
        
        if github:
            owner, private, license = SharedMenus.get_github_info(
                get_license=True
            )

            self.__create_github_repo(
                name=name,
                owner=owner,
                directory=directory,
                private=private,
                auto_init="true",
                clone=False,
                license=license,
                language=language
            )

        apps = SharedMenus.select_apps()
        urls = SharedMenus.select_urls()

        self.__save_workspace(
            directory=directory,
            name=name,
            apps=apps,
            urls=urls,
            owner=owner or None,
            private=private or None
        )

    # Import an exiting project as a WorkSpace
    def import_workspace(self, **kwargs) -> None:

        name, directory, github, language = SharedMenus.get_workspace_info(
            directories=self.settings["folders"],
            languages=self.settings["languages"].keys(),
            get_language=False,
            kwargs=kwargs
        )

        if name in os.listdir(directory):
            raise WorkSpaceAlreadyExists("This name is already being used")
        
        if github:
            owner, private, license = SharedMenus.get_github_info(
                get_license=False
            )

            self.__create_github_repo(
                name=name,
                owner=owner,
                directory=directory,
                private=private,
                auto_init="false",
                clone=False
            )

        apps = SharedMenus.select_apps()
        urls = SharedMenus.select_urls()

        self.__save_workspace(
            directory=directory,
            name=name,
            apps=apps,
            urls=urls,
            owner=owner or None,
            private=private or None
        )

    # Delete an existing WorkSpace
    def delete_workspace(self, **kwargs) -> None:

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
            API_KEY=self.api_key,
            name=name,
            owner=owner,
            directory=directory)
        
        ContentsManager()

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w") as f:
            json.dump(data, f)

    # Open VSCode, APPs and URLs associated to a WorkSpace
    def open_workspace(self, **kwargs) -> None:

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto")
        if name not in data:
            raise WorkSpaceNotFound("No se encontró el workspace con ese nombre.")

        directory = data[name]["directory"]
        profile = SharedMenus.select_vscode_profile(vscode_settings=self.settings["vscode"]["path"])

        apps = data[name]["apps"].items()
        urls = data[name]["urls"]

        AppsManager()
        WebsManager()

    # Publish a WorkSpace to GitHub
    def publish_workspace(self, **kwargs) -> None:

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Introduce el nombre del proyecto")
        owner = kwargs.get("owner") or inquirer.list_input("¿Quién es el propietario del repositorio?")
        private = kwargs.get("private") or "true" if inquirer.confirm("¿El repositorio es privado?", default=False) else "false"

        if name not in data:
            raise WorkSpaceNotFound("No se encontró el workspace con ese nombre.")

        self.__create_github_repo(
            name=name,
            owner=owner,
            directory=data[name]["directory"],
            private=private,
            auto_init="false",
            clone=False
        )

        data[name]["owner"] = owner
        data[name]["private"] = private

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "w") as f:
            json.dump(data, f)

    # Move an existing WorkSpace to another Path
    def move_workspace(self, **kwargs) -> None:

        name, new_directory = SharedMenus.get_move_workspace_info(
            directories=self.settings["folders"],
            kwargs=kwargs
        )

        if not inquirer.confirm(f"Want to move the workspace {name}?") and not self.yes:
            print("Exiting...")
            return None

        ContentsManager()

        with open(os.path.join(MAIN_DIRECTORY, "workspaces.json"), "r+") as f:
            data = json.load(f)

        data[name]["directory"] = os.path.join(new_directory, name)

        with open(os.path.join(MAIN_DIRECTORY, "workspace.json"), "w") as f:
            json.dump(data, f)

    # Edit the information of an existing repo
    def edit_workspace(self, **kwargs) -> None:

        with open(os.path.join(MAIN_DIRECTORY, "workspace.json"), "r+") as f:
            data = json.load(f)

        if kwargs.get("add-apps"):
            apps = SharedMenus.select_apps()
            data["apps"] += apps

        if kwargs.get("del-apps"):
            apps_to_delete = inquirer.Checkbox("apps", message="Selecciona las aplicaciones a eliminar.", choices=data["apps"].keys())
            for app in inquirer.prompt([apps_to_delete])["apps"]:
                del data["apps"][app]

        if kwargs.get("add-urls"):
            urls = SharedMenus.select_urls()
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

    # Save a WorkSpace thats being currently editted
    def __save_workspace(self,
        directory: str,
        name: str,
        apps: dict,
        urls: list,
        owner: str = None,
        private: str = None
        ) -> None:
        
        if not inquirer.confirm("Want to create the WorkSpace?") and not self.yes:
            print("Exiting...")
            return None

        spinner = yaspin(text=" Saving the WorkSpace...")
        spinner.start()

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

        spinner.stop()

    # Create a GitHub repo
    def __create_github_repo(self,
        name: str,
        owner: str,
        directory: str,
        private: str,
        auto_init: str,
        clone: bool,
        license: str = None,
        language: str = None,
        ) -> None:

        if not inquirer.confirm("Want to create the repo?") and not self.yes:
            print("Exiting...")
            return None

        action = 0 if owner == self.settings["git-user"] else 1

        github = Github(
            action=action,
            clone=clone,
            API_KEY=self.api_key,
            name=name,
            owner=owner,
            directory=directory,
            private=private,
            auto_init=auto_init,
            license=license,
            language=language
        )

        github.push_user_repo()
