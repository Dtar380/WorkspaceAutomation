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
from .builders import Github
from .builders import ContentsManager

# RUNNERS
from .runners import run_apps
from .runners import open_urls

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from ..__vars__ import settings_paths, languages

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[os.system()]

##### DEFINE MAIN FILES DIRECTORIES
WORKSPACES = os.path.join(MAIN_DIRECTORY, "workspaces.json")

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

        # Valid commands
        commands = {
            "create": self.create_workspace,
            "import": self.import_workspace,
            "delete": self.delete_workspace,
            "open": self.open_workspace,
            "publish": self.publish_workspace,
            "move": self.move_workspace,
            "edit": self.edit_workspace,
        }

        # Run selected command
        commands[command](**kwargs)

    ##### WORKSPACE FUNCTIONS
    # Create a new WorkSpace
    def create_workspace(self, **kwargs) -> None:

        name, directory, github, language = SharedMenus.get_workspace_info(
            directories=self.settings["directories"],
            languages=self.settings["languages"].keys(),
            get_language=True,
            kwargs=kwargs
        )

        if name in os.listdir(directory):
            raise WorkSpaceAlreadyExists("A WorkSpace with this name already exists.")

        if github:
            owner, private, license = SharedMenus.get_github_info(
                default_owner=self.settings["github_user"],
                get_license=True,
                kwargs=kwargs
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

        ContentsManager(
            action=1,
            directory=directory,
            name=name,
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
            directories=self.settings["directories"],
            languages=self.settings["languages"].keys(),
            get_language=False,
            kwargs=kwargs
        )

        if name in os.listdir(directory):
            raise WorkSpaceAlreadyExists("A WorkSpace with this name already exists.")

        if github:
            owner, private, license = SharedMenus.get_github_info(
                default_owner=self.settings["github_user"],
                get_license=False,
                kwargs=kwargs
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

        with open(WORKSPACES, "r+") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Enter the name of your WorkSpace")
        if name not in data:
            raise WorkSpaceNotFound("There was no WorkSpace found with that name.")

        directory = data[name]["directory"]
        owner = data[name]["owner"]

        if inquirer.confirm(f"Want to delete the WorkSpace {name}?") and not self.yes:
            ContentsManager(
                actions=2,
                directory=directory,
                name=name
            )

        elif inquirer.confirm(f"Want to delete the repo {name}?") and self.yes:
            Github(
                action=2,
                clone=False,
                API_KEY=self.api_key,
                name=name,
                owner=owner,
                directory=directory
            )

        else:
            print("exiting...")
            return None

        del data[name]

        with open(WORKSPACES, "w+") as f:
            json.dump(data, f)

    # Open VSCode, APPs and URLs associated to a WorkSpace
    def open_workspace(self, **kwargs) -> None:

        with open(WORKSPACES, "r+") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Enter the name of your WorkSpace")
        if name not in data.keys():
            raise WorkSpaceNotFound("There was no WorkSpace found with that name.")

        directory = data[name]["directory"]
        profile = SharedMenus.select_vscode_profile(vscode_settings=self.settings["vscode"]["path"])

        apps = data[name]["apps"].values()
        urls = data[name]["urls"]

        # RUNNERS
        run_apps(directory=directory, apps=apps, profile=profile)
        open_urls(urls=urls)

    # Publish a WorkSpace to GitHub
    def publish_workspace(self, **kwargs) -> None:

        with open(WORKSPACES, "r+") as f:
            data = json.load(f)

        name = kwargs.get("name") or inquirer.text("Enter the name of your WorkSpace")
        owner, private, license = SharedMenus.get_github_info(
            default_owner=self.settings["github_user"],
            get_license=True,
            kwargs=kwargs
        )

        if name not in data.keys():
            raise WorkSpaceNotFound("There was no WorkSpace found with that name.")

        language = data[name]["language"] or None

        self.__create_github_repo(
            name=name,
            owner=owner,
            directory=data[name]["directory"],
            private=private,
            auto_init="false",
            clone=False,
            license=license,
            language=language
        )

        data[name]["owner"] = owner
        data[name]["private"] = private

        with open(WORKSPACES, "w+") as f:
            json.dump(data, f)

    # Move an existing WorkSpace to another Path
    def move_workspace(self, **kwargs) -> None:

        name, new_directory = SharedMenus.get_move_workspace_info(
            directories=self.settings["directories"],
            kwargs=kwargs
        )

        with open(WORKSPACES, "r+") as f:
            data = json.load(f)

        if name not in data.keys():
            raise WorkSpaceNotFound("There was no WorkSpace found with that name.")

        if not inquirer.confirm(f"Want to move the WorkSpace {name}?") and not self.yes:
            print("Exiting...")
            return None

        ContentsManager(
            action=1,
            directory=data[name]["directory"],
            name=name,
            new_directory=new_directory
        )

        data[name]["directory"] = os.path.join(new_directory, name)

        with open(WORKSPACES, "w+") as f:
            json.dump(data, f)

    # Edit the information of an existing repo
    def edit_workspace(self, **kwargs) -> None:

        with open(WORKSPACES, "r+") as f:
            data = json.load(f)

        # ADD APPS TO WORKSPACE
        if kwargs.get("add-apps"):
            apps = SharedMenus.select_apps()
            data["apps"] += apps

        # REMOVE APPS FROM WORKSPACE
        if kwargs.get("del-apps"):
            apps_to_delete = inquirer.Checkbox("apps", message="Please select the APPs to remove.", choices=data["apps"].keys())
            for app in inquirer.prompt([apps_to_delete])["apps"]:
                del data["apps"][app]

        # ADD URLS TO WORKSPACE
        if kwargs.get("add-urls"):
            urls = SharedMenus.select_urls()
            data["urls"].extend(urls)

        # DELETE URLS FROM WORKSPACE
        if kwargs.get("del-urls"):
            urls_to_delete = inquirer.Checkbox("urls", message="Please select the URLs to remove.", choices=data["urls"])
            for url in inquirer.prompt([urls_to_delete])["urls"]:
                data["urls"].remove(url)

        if not inquirer.confirm("Want to perform changes?") and not self.yes:
            print("Exiting...")
            return None

        with open(WORKSPACES, "r+") as f:
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

        with open(WORKSPACES, "r+") as f:
            data = json.load(f)

        data[name] = {
            "directory": os.path.join(directory, name),
            "apps": apps,
            "urls": urls,
            "owner": owner,
            "private": private
        }

        with open(WORKSPACES, "w+") as f:
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

        gitignore = languages[language] or None

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
            gitignore=gitignore
        )

        github.push_user_repo()
