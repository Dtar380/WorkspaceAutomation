########################################
#####  IMPORTING MODULES           #####
########################################

from pathlib import Path

########################################
#####  CODE                        #####
########################################

#####  GLOBAL VARIABLES
# Path to settings
settings_paths = {
    "Windows": str(Path.home()) + "\\AppData\\Roaming\\WorkSpaceAutomation",
    "Darwin": str(Path.home()) + "\\Library\\Application\\ Support\\WorkSpaceAutomation",
    "Linux": str(Path.home()) + "\\.config\\WorkSpaceAutomation"
}

# Path to vscode settings
code_paths = {
    "Windows": str(Path.home()) + "\\AppData\\Roaming\\{}\\User\\globalStorage\\storage.json",
    "Darwin": str(Path.home()) + "\\Library\\Application\\ Support\\{}\\User\\globalStorage\\storage.json",
    "Linux": str(Path.home()) + "\\.config\\{}\\User\\globalStorage\\storage.json"
}

languages = {
    "Python": {
        "gitignore": "",
        "directories": [

        ],
        "files": [

        ],
        "venv-command": ""
    },
}
