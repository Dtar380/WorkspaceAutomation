########################################
#####  IMPORTING MODULES           #####
########################################

#####  EXTERNAL IMPORTS
# OPENING URLS
import webbrowser
import time

########################################
#####  FUNCTION                    #####
########################################

# OPENS ALL URLS
def open_urls(urls) -> None:

    for url in urls:
        webbrowser.open(url)
        time.sleep(0.5)
