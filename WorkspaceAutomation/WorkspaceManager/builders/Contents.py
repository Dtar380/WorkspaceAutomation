########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
# ENV MANAGEMENT
import shutil
import os

# CLI
from yaspin import yaspin

########################################
#####  CODE                        #####
########################################

#####  GLOBAL VARIABLES
from ...__vars__ import settings_paths, languages

##### DEFINE MAIN DIRECTORY ACCORDING TO OPERATING SYSTEM
MAIN_DIRECTORY = settings_paths[os.system()]

########################################
#####  CLASS                       #####
########################################

class ContentsManager:

    ##### INITIALISE CLASS
    @yaspin(text="Setting up WorkSpace...")
    def __init__(self,
        action: int,
        directory: str,
        name: str,
        language: str = None,
        new_directory: str = None
        ) -> None:
        
        # All actions in a list
        actions = [
            self.create_workspace,
            self.move_workspace,
            self.delete_workspace
        ]

        # Set given parameters as class variables
        self.directory = directory
        self.name = name
        self.language = language
        self.new_directory = new_directory

        # Create new class variables from given parameters
        self.workspace_folder = os.path.join(self.directory, self.name)
        self.new_workspace_folder = os.path.join(self.new_directory, self.name) or None

        # Execute action requested
        actions[action]()

    ##### CREATE ALL FOLDERS AND FILES ACCORDING TO THE LANGUAGE SELECTED
    def create_workspace(self) -> None:

        os.makedirs(self.workspace_folder, exist_ok=True)
        os.chdir(self.workspace_folder)
        
        directories: list = languages[self.language]["directories"]
        files: list = languages[self.language]["files"]
        venv_command: str = languages[self.language]["venv-command"]

        directories.extend([
            ".vscode"
        ])

        files.extend([
            ".vscode/settings.json"
        ])
        
        for directory in directories:
            os.makedirs(directory)

        for file in files:
            with open(file, "x+") as f:
                pass

        if venv_command:
            os.system(venv_command)

    ##### MOVE SELECTED WORKSPACE TO NEW LOCATION
    def move_workspace(self) -> None:
        shutil.move(self.workspace_folder, self.new_workspace_folder)
        self.delete_workspace()

    ##### DELETE ALL FOLDERS AND FILES FROM A WORKSPACE
    def delete_workspace(self) -> None:
        shutil.rmtree(self.workspace_folder)
