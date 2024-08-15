########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
import subprocess
import os

########################################
#####  GLOBAL VARIABLES            #####
########################################

##### IMPORT GLOBAL VARIABLES FROM FILE
from ...__vars__ import settings_paths

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[os.system()]

##### DEFINE MAIN FILES DIRECTORIES
WORKSPACES = os.path.join(MAIN_DIRECTORY, "workspaces.json")

########################################
#####  FUNCTION                    #####
########################################

def run_apps(directory: str, apps: list, profile: str) -> None:
        
    # Run VSCode with selected profile on selected directory
    subprocess.run(["powershell.exe", "-c", f"code-insiders --profile {profile} {directory}"])
    
    # Try to run GitHub on selected directory
    try:
        subprocess.run(["powershell.exe", "-c", f"github {directory}"])
    except:
        pass

    # Run all apps for selected WorkSpace
    for app in apps:

        # Try to run the app
        try:
            subprocess.run(app)
        except:
            pass
