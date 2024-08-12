########################################
#####  DOCUMENTATION               #####
########################################

'''

'''

########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
from yaspin import yaspin
import requests
import subprocess
from os import chdir, system
from os.path import join, exists

########################################
#####  CODE                        #####
########################################

#####  GLOBAL VARIABLES
from ..__vars__ import settings_paths
GITHUB_API = "https://api.github.com"

# MOVE TO SETTINGS PATH
MAIN_DIRECTORY = settings_paths[system()]

#####  CLASS
class Github:

    def __init__(self, action: int, clone: bool, API_KEY: str, directory: str, name:str, owner: str, **kwargs) -> None:
        
        self.headers = {
        "Authorization": "Bearer " +  API_KEY,
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
                private = kwargs["private"]
                auto_init = kwargs["auto_init"]
                if auto_init == "true":
                    gitignore = kwargs["gitignore"]
                    license = kwargs["license"]
            except:
                raise Exception("Missing arguments")
        
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
        print(payload)
        print(self.headers)
        requests.post(GITHUB_API+"/user/repos", data=payload, headers=self.headers)

    @yaspin(text="Creating GitHub Repository...")
    def __create_org_repo(self, payload) -> None:
        requests.post(GITHUB_API+f"/orgs/{self.owner}/repos", data=payload, headers=self.headers)

    @yaspin(text="Deleting GitHub Repository...")
    def __delete_repo(self) -> None:
        requests.delete(GITHUB_API+f"/repos/{self.owner}/{self.name}", headers=self.headers)

    @yaspin(text="Cloning GitHub Repository...")
    def __clone_repo(self) -> None:
        chdir(join(self.directory, self.name))
        url = f"https://github.com/{self.owner}/{self.name}.git"
        system("git clone" + url)
        chdir(MAIN_DIRECTORY)

    @yaspin(text="Pushing project to github")
    def push_user_repo(self) -> None:
        chdir(join(self.directory, self.name))

        if not exists("README.md"):
            system('ECHO #' + self.name + ' >> README.md')
        system("git init")
        system("git add . && git commit -m 'Initial Commit' && git branch -M main")
        system(f"git remote add origin http://{self.TOKEN}@github.com/{self.owner}/{self.name}.git")
        system("git push -u origin main")
        chdir(MAIN_DIRECTORY)