#######################################
#####  IMPORT MODULES  ################
#######################################

from pathlib import Path

#######################################
#####  CODE  ##########################
#######################################

##### GLOBAL VARIABLES
# Path to settings
settings_paths = {
    "Windows": str(Path.home()) + "\\AppData\\Roaming\\WorkSpaceAutomation",
    "Darwin": str(Path.home()) + "\\Library\\Application\\ Support\\WorkSpaceAutomation",
    "Linux": str(Path.home()) + "\\.config\\WorkSpaceAutomation"
}
