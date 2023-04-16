###############################################
###############################################
# ADD HERE
###############################################

import os

from calcs import *
import dialogs

##########################################
if __name__ == "__main__":
    # I can't figure out how to play nice with small screens - help me pluz..
    if os.get_terminal_size().lines < dialogs.MAX_TALL:
        print("your terminal is too small... we need at least 25 lines")
        exit(1)

    # simulate -f=myminer.csv #TODO try this??
    #if len(sys.argv) > 1:
    #    load_csv( sys.argv[1] ) # try to load first file
    # TODO - look for myminers.csv
    # if found:
    #   load miners variable in globalz
    #   pop up to user - loaded myminers.csv (optionally list miners found.  ACTION_USE, ACTION_DON'T_USE aka start fresh)

    # WELCOME SCREEN
    #dialogs.PopUp("welcome", "add your miners and press 'simulate' to play ;)")

    # MAIN() LOOP OF APPLICATION
    while True:
        if not dialogs.dialog_main(): #if it returns false, exit
            break

    print('<3 happy hashing <3 ', end='')
    #RETURN FALSE; DONE DONE DONE DONE DONE DONE DOBE DONDONE DOBE DOB EDOBE JINX!!! HAHAHAHAHA



###############################################
###############################################
# what i learned...
###############################################
# https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
# with Context()
