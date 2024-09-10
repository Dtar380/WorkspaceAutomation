########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
# ENV MANAGEMENT
import os
import platform

# HTTP REQUESTS
import requests

# CLI
from yaspin import yaspin

##### INTERNAL IMPORTS
# ERRORS
from ...__errors__ import *

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from ...__vars__ import settings_paths

GITHUB_API = "https://api.github.com" # GitHub API URL

##### DEFINE MAIN DIRECTORY
MAIN_DIRECTORY = settings_paths[platform.system()]

########################################
#####  CLASS                       #####
########################################

class Github:

    def __init__(self,
        action: int,
        clone: bool,
        API_KEY: str,
        name:str,
        owner: str,
        directory: str,
        **kwargs
        ) -> None:

        self.TOKEN = API_KEY

        self.headers = {
        "Authorization": "Bearer " +  self.TOKEN,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
        }

        functions = [
            self.__create_user_repo,
            self.__create_org_repo,
            self.__delete_repo
        ]

        if kwargs:
            try:
                private = kwargs.get("private")
                auto_init = kwargs.get("auto_init")
                gitignore = kwargs.get("gitignore") if auto_init == "true" else None
                license = kwargs.get("license") if auto_init == "true" else None
            except:
                raise MissingArguments("There are missing arguments, please re-run the command")

        self.directory = directory
        self.owner = owner
        self.name = name

        if action in (0,1):

            if auto_init == "true":
                payload = '{"name":"' + self.name + '","private":' + private + ',"auto_init":' + auto_init + ',"gitignore_template":"' + gitignore +  '","license_template":"' + license + '"}'
            else:
                payload = '{"name":"' + self.name + '","private":' + private + ',"auto_init":' + auto_init + '"}'
            functions[action](payload)

        elif action == 2:
            functions[action]()

        if clone:
            self.__clone_repo()

    @yaspin(text="Creating GitHub Repository...")
    def __create_user_repo(self, payload) -> None:
        requests.post(GITHUB_API+"/user/repos", data=payload, headers=self.headers)

    @yaspin(text="Creating GitHub Repository...")
    def __create_org_repo(self, payload) -> None:
        requests.post(GITHUB_API+f"/orgs/{self.owner}/repos", data=payload, headers=self.headers)

    @yaspin(text="Deleting GitHub Repository...")
    def __delete_repo(self) -> None:
        requests.delete(GITHUB_API+f"/repos/{self.owner}/{self.name}", headers=self.headers)

    @yaspin(text="Cloning GitHub Repository...")
    def __clone_repo(self) -> None:
        os.chdir(os.path.join(self.directory, self.name))
        url = f"https://github.com/{self.owner}/{self.name}.git"
        os.system("git clone" + url)
        os.chdir(MAIN_DIRECTORY)

    @yaspin(text="Pushing project to github")
    def push_user_repo(self) -> None:
        os.chdir(os.path.join(self.directory, self.name))

        if not os.path.exists("README.md"):
            os.system('ECHO #' + self.name + ' >> README.md')

        os.system("git init")
        os.system("git add . && git commit -m 'Initial Commit' && git branch -M main")
        os.system(f"git remote add origin http://{self.TOKEN}@github.com/{self.owner}/{self.name}.git")
        os.system("git push -u origin main")
        os.chdir(MAIN_DIRECTORY)
