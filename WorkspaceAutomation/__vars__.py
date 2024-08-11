########################################
#####  DOCUMENTATION               #####
########################################

'''

'''

########################################
#####  IMPORTING MODULES           #####
########################################

from pathlib import Path

########################################
#####  CODE                        #####
########################################

#####  GLOBAL VARIABLES
settings_paths = {
    "Windows": str(Path.home()) + f"\\AppData\\Roaming\\WorkSpaceAutomation",
    "Darwin": str(Path.home()) + f"\\Library\\Application\\ Support\\WorkSpaceAutomation",
    "Linux": str(Path.home()) + f"\\.config\\WorkSpaceAutomation"
}

code_paths = {
    "Windows": str(Path.home()) + "\\AppData\\Roaming\\{}\\User\\globalStorage\\storage.json",
    "Darwin": str(Path.home()) + "\\Library\\Application\\ Support\\{}\\User\\globalStorage\\storage.json",
    "Linux": str(Path.home()) + "\\.config\\{}\\User\\globalStorage\\storage.json"
}