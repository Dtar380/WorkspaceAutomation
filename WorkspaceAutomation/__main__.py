##################################################
#####     IMPORTS                            #####
##################################################

#####  EXTERNAL IMPORTS
# ENV AND PATHS
import os
import platform

# CLI
import argparse


##### INTERNAL IMPORTS
# ERRORS
from .__errors__ import *

# APP
from .app import App
from .set_up import SetUp
##################################################
#####     CODE                               #####
##################################################

from .__vars__ import settings_paths

#####  DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[platform.system()]

##################################################
#####     CLASS                              #####
##################################################

class Renderer:

    def __init__(self) -> None:

        ## PARSER
        self.parser = argparse.ArgumentParser(
            usage=f"""
General Usage:
%(prog)s [-h] [-v]

Set-Up:
%(prog)s [-i] [-k KEY] [--vscode VS_CODE] [--set-up-languages LANGUAGES] [--custom-dir CUSTOM_DIR] [--create-folders] [--github-user GITHUB_USER] [--api-key API_KEY] [-y]

Command:
%(prog)s [-c COMMAND] [-k KEY] [--name NAME] [--directory DIRECTORY] [--language LANGUAGE] [--github GITHUB] [--owner OWNER] [--private PRIVATE] [--license LICENSE] [--new-directory NEW_DIRECTORY] [--add-apps ADD_APPS] [--del-apps DEL_APPS] [--add-urls ADD_URLS] [--del-urls DEL_URLS] [-y]

SubCommand:
%(prog)s [-c \"config\"] [-sc SUB_COMMAND] [-k KEY] [--vscode VS_CODE] [--setup-languages LANGUAGES] [--custom-dir CUSTOM_DIR] [--create-folders] [--github-user GITHUB_USER] [--api-key API_KEY] [-y]""")

        ## GENERAL ARGUMENTS
        self.parser.add_argument('-v', '--version', action='version', version='Current version is ' + "0.1.0", help='Gives the version of the program')

        ## MAIN
        self.parser.add_argument('-i', '--init', action='store_true', help='Initialise the program')
        self.parser.add_argument('-c', '--command', action='store', type=str, help='Enter a command to run')
        self.parser.add_argument('-sc', '--sub-command', action='store', type=str, help='Enter a sub-command if required')
        self.parser.add_argument('-k', '--key', action='store', type=str, help='Enter your key')
        self.parser.add_argument('-y', '--yes', action='store_true', help='Confirm')

        ## SET-UP
        self.parser.add_argument('--vscode', action='store', type=str, help='Enter your VSCode version type (code/insiders)')
        self.parser.add_argument('--set-up-languages', action='store', type=str, help='Enter a comma separated list of languages to install')
        self.parser.add_argument('--custom-dir', action='store', type=str, help='Path if you want to use a custom directory')
        self.parser.add_argument('--create-directories', action='store_true', help='Set if you want to create new folders for the workspaces')
        self.parser.add_argument('--github-user', action='store', type=str, help='Enter your GitHub username')
        self.parser.add_argument('--api-key', action='store', type=str, help='Enter your GitHub API key')

        ### APP
        ## APP INFO
        self.parser.add_argument('--name', action='store', type=str, help='Enter your project name')
        self.parser.add_argument('--directory', action='store', type=str, help='Enter the directory of your project')
        self.parser.add_argument('--language', action='store', type=str, help='Enter the language of your project')

        ## APP GITHUB
        self.parser.add_argument('--github', action='store_true', help='Enter if you want to create a GitHub repo')
        self.parser.add_argument('--owner', action='store', type=str, help='Enter the owner of the repo')
        self.parser.add_argument('--private', action='store_true', help='Set if you want to create a private repo')
        self.parser.add_argument('--license', action='store', type=str, help='Enter the license of the repo')

        ## APP MOVE
        self.parser.add_argument('--new-directory', action='store', type=str, help='Enter the directory you want to move the workspace to')

        ## APP EDIT
        self.parser.add_argument('--add-apps', action='store_true', help='Command for adding new apps to the workspace')
        self.parser.add_argument('--del-apps', action='store_true', help='Command for deleting apps from the workspace')
        self.parser.add_argument('--add-urls', action='store_true', help='Command for adding new URLs to the workspace')
        self.parser.add_argument('--del-urls', action='store_true', help='Command for deleting URLs from the workspace')

    # Main Function
    def main(self) -> None:

        arguments = vars(self.parser.parse_args())

        # Check if key is provided
        if not arguments.get("key"):
            raise PasswordNotProvided("The password must be provided.")

        # Check if app was already initialised
        if not os.path.exists(MAIN_DIRECTORY) and not arguments.get("init"):
            raise AppNotInitialised("""The app is not set-up. Please run "--init" command.""")

        # Run the program with the provided arguments
        if arguments.get("init"):
            SetUp(
                key=arguments["key"],
                kwargs=arguments
            )
        elif arguments.get("command"):
            App(
                key=arguments["key"],
                command=arguments["command"],
                sub_command=arguments["sub_command"],
                kwargs=arguments
            )

#####  RUN FILE
if __name__ == "__main__":
    renderer = Renderer()
    renderer.main()
