###############################################
###############################################
# ADD HERE
###############################################
import os
from picotui.context import Context
from picotui.screen import Screen
from picotui.widgets import *
from picotui.defs import *

from calcs import *

MAX_TALL=25

###############################################
## application-specific button commands
ACTION_ADDMINER=7070
ACTION_REMOVEMINER=6969
ACTION_SIMULATE=7171
ACTION_QUIT=7373

###############################################
def PopUp(title: str, info: str) -> None:
    with Context():
        d = Dialog(0, 0, len(info)+4, 4)

        d.add(len(info)/2 - len(title)/2 , 0, title.upper())

        d.add(2, 2, info)
        b = WButton(" OK ")
        d.add(len(info)/2 - 3, 4, b)
        b.finish_dialog = ACTION_OK

        res = d.loop()
###############################################
def dialog_add_miner():
    #TODO - CHECK IF CONSOLE SCREEN IS EVEN BIG ENOUGH
    FAT = 23
    TALL = 10
    
    with Context():
        d = Dialog(0, 0, FAT, TALL)

        d.add(1, 0, "ADD MINER:")
        d.add(1, 2, "name -------")
        d.add(1, 4, "wattage ----")
        d.add(1, 6, "eff (w/th) -")
        d.add(1, 8, "quantity ---")

        w = WTextEntry(12, "")
        w.tag = "name"
        d.add(14, 2, w)

        w = WTextEntry(5, "")
        w.tag = "wattage"
        d.add(14, 4, w)

        w = WTextEntry(5, "")
        w.tag = "eff"
        d.add(14, 6, w)

        w = WTextEntry(5, "1")
        w.tag = "quantity"
        d.add(14, 8, w)

        b = WButton("ADD")
        d.add(2, TALL, b)
        b.finish_dialog = ACTION_OK
        
        b = WButton(" X ")
        d.add(FAT, 0, b)
        b.finish_dialog = ACTION_CANCEL

    # WAIT FOR AN ACTION BUTTON
        res = d.loop()

    # QUIT BUTTON
    if res == ACTION_CANCEL:
        return
    
    # OK BUTTON
    if res == ACTION_OK:
        # GO THRU EVERY UI ITEM AND GRAB ITS DATA
        data = {}
        for w in d.childs:
            if isinstance(w, EditableWidget):
                val = w.get()
                if val is not None:
                    data[w.tag] = val

        # MAKE SURE USER ENTERED NUMBRES
        try:
            data["wattage"] = int(data["wattage"])
            data["eff"] = int(data["eff"])
            data["quantity"] = int(data["quantity"])
            # NOTE - IF THE USER ENTERS BAD DATA, THEY GET BAD RESULTS.. WE CAN'T DO EVERYTHING FOR THEM.  DIVIDE BY ZERO ALL YOU WANT!

        # MAKE GLOBAL CHANGE TO MINERS DATA
            miners.append( data )

        # IF WE DID NOT ENTER NUMBERS
        except ValueError:
            PopUp("input error", "wattage, eff and quantity have to be numbers")
###############################################
def dialog_remove_miner():
    FAT = 40
    TALL = len(miners) + 9
    
    with Context():
        d = Dialog(0, 0, FAT, TALL)
        #d = Dialog(0, 0) # I guess I don't need sizez... jahumm... :/

        ####### YOUR MINERS
        left = 1
        top = 4
        d.add(left, top, WFrame(FAT, len(miners)+3, "Your miners:"))
        for i, m in enumerate(miners):
            st = "{}: {} ( {} watts @ {} W/Th ) x {}".format(1+i, m["name"], m["wattage"], m["eff"], m["quantity"])
            d.add(left+1, top+2+i, st)

        # TITLE
        d.add(1, 0, "REMOVE MINER:")

        # INPUT
        #d.add(1, 2, WFrame(15, 3, "index # "))
        d.add(1, 2, "index #:")

        w = WTextEntry(4, "")
        w.tag = "index" # WHAT THE DATA IS CALLED
        d.add(7, 2, w) # ADD TO FORM!

        # OK / YES BUTTON
        b = WButton("REMOVE")
        d.add(2, TALL-1, b)
        b.finish_dialog = ACTION_OK # THIS MAKES IT AN ACTION BUTTON
        
        # X BUTTON CLOSES OUT
        b = WButton(" X ")
        d.add(FAT-4, 0, b)
        b.finish_dialog = ACTION_CANCEL

        res = d.loop() # WAIT FOR ACTION BUTTON

    #################################
    if res == ACTION_CANCEL:
        return

    if res == ACTION_OK:
        data = {}
        for w in d.childs:
            if isinstance(w, EditableWidget):
                val = w.get()
                if val is not None:
                    data[w.tag] = val
        try:

            idx = int(data["index"]) - 1

            if idx < 0 or idx > len(miners)-1:
                raise IndexError()
            
            #miners.remove( int(data["index"]) )  # THIS DOES NOT WORK!!!
            del miners[ idx ]

        except ValueError:
            PopUp("ERROR", "pick the index number from the 'your miners:' list")
        except IndexError:
            PopUp("ERROR", "no such index number")
#######################################
def dialog_simulate():
    FAT=40
    TALL=MAX_TALL

    with Context():
        d = Dialog(0, 0, FAT, TALL) # as big as it needs to be?
        
        # RUN BUTTON
        b = WButton(" RUN! ")
        d.add(1, 1, b)
        b.finish_dialog = ACTION_OK

        # INSTRUCTIONS TO THE USER #########################
        d.add(1, 2, "Simulate possible scenarios based on")
        d.add(1, 3, "future projection of price and hashrate.")
        d.add(1, 4, "Try different strategies, too.")

        ######## PROJECTION VARIABLES
        left = 1
        top = 6
        d.add(left, top, WFrame(FAT, 5, "PROJECTION VARIABLES:"))
        d.add(left+1, top+2, "price growth (annual)       %")
        d.add(left+1, top+3, "hashrate growth (annual)    %")

        w = WTextEntry(3, "6")
        w.tag = "price_growth" # WHAT THE DATA IS CALLED
        #w.content = str( 6 ) # START WITH DEFAUL 6% GROWTH TODO - MAYBE HAVE IT CALCULATE HISTORICAL AND PLACE THAT VALUE IN HERE INSTEAD OF JUST HARD CODING SOMETHING
        d.add(left+26, top+2, w) # ADD TO FORM!

        w = WTextEntry(3, "12")
        w.tag = "hash_growth" # WHAT THE DATA IS CALLED
        #w.content = str( 12 ) # START WITH DEFAUL 12% GROWTH
        d.add(left+26, top+3, w) # ADD TO FORM!

        ######## COSTS
        left = 1
        top = 11
        d.add(left, top, WFrame(FAT, 6, "YOUR COSTS:"))
        d.add(left+1, top+2, "$ per kWh -----")
        d.add(left+1, top+3, "$ CAPEX -------")
        d.add(left+1, top+4, "$ daily OPEX --")

        w = WTextEntry(5, "0.12")
        w.tag = "cost_kWh" # WHAT THE DATA IS CALLED
        d.add(left+17, top+2, w) # ADD TO FORM!

        w = WTextEntry(5, "0")
        w.tag = "CAPEX" # WHAT THE DATA IS CALLED
        d.add(left+17, top+3, w) # ADD TO FORM!

        w = WTextEntry(5, "0")
        w.tag = "daily_OPEX" # WHAT THE DATA IS CALLED
        d.add(left+17, top+4, w) # ADD TO FORM!

        ######## YOUR STRATEGY
        left = 1
        top = 20
        d.add(left, top, WFrame(FAT, 5, "YOUR STRATEGY:"))
        d.add(left+1, top+2, "sell: >DROP DOWN<")

        # BACK BUTTON
        b = WButton(" X ")
        d.add(FAT - 3, 1, b)
        b.finish_dialog = ACTION_CANCEL

        res = d.loop()

    # run simulation
    if res == ACTION_OK:
        PopUp("RESULTS", "... are shown here")
        
        return True # don't keep going

        # verify input fields... collect data
        # RUN_SIMULATION( env variables )
        # dialog_results()
    
    if res == ACTION_CANCEL:
        return False # keep running
#######################################
def dialog_main():
    FAT=60
    #TALL = len(miners) + 20

    with Context():
        #d = Dialog(0, 0, FAT, TALL)
        d = Dialog(0, 0)

        b = WButton("ADD MINER")
        d.add(1, 1, b)
        b.finish_dialog = ACTION_ADDMINER

        if len(miners):
            b = WButton("REMOVE")
            d.add(13, 1, b)
            b.finish_dialog = ACTION_REMOVEMINER

        ####### YOUR MINERS
        left = 1
        top = 3
        d.add(left, top, WFrame(FAT, len(miners)+3, "YOUR MINERS:"))
        for i, m in enumerate(miners):
            st = "{}: {} ( {} watts @ {} W/Th ) x {}".format(1+i, m["name"], m["wattage"], m["eff"], m["quantity"])
            d.add(left+1, top+2+i, st)
        
        ####### YOUR STATS
        left = 1
        top = len(miners)+7
        d.add(left, top, WFrame(FAT, 6, "YOUR STATS:"))
        d.add(left+1, top+2, "total wattage ---")
        d.add(left+1, top+3, "total terahash --")
        d.add(left+1, top+4, "avg eff (w/th) --")

        if not len(miners):
            d.add(left + 22, top + 3, "> ADD MINERS TO SEE STATS <")
        else:
            d.add(left+19, top+2, str(total_wattage()) )
            d.add(left+19, top+3, str(total_hr()) )        
            d.add(left+19, top+4, str(total_eff()) )

        ###### NETWORK STATS
        left = 1
        top = len(miners)+14
        d.add(left+0, top, WFrame(36, 9, "NETWORK STATS:"))
        d.add(left+1, top+2, "difficulty --------")
        d.add(left+1, top+3, "network hashrate --") #UNITS?
        d.add(left+1, top+5, "block height ------")
        d.add(left+1, top+6, "subsidy -----------")
        d.add(left+1, top+7, "avg fees ----------")

        d.add(left+21, top+2, str( 1234567890 ).zfill(12))
        d.add(left+21, top+3, "***")
        d.add(left+21, top+5, "***")
        d.add(left+21, top+6, "***")
        d.add(left+21, top+7, "***")

        ###### PRICE
        left = 37
        d.add(left, top+0, WFrame(24, 5, "PRICE:"))
        d.add(left + 1, top+2, "one btc = ")
        d.add(left + 1, top+3, "one sat = ")

        d.add(left + 11, top+2, "$ " + str(price_btc))
        d.add(left + 11, top+3, "$ " + str(price_sat)[0:9]) #only 8 chars

        ####### PROFIT / LOSS
        top = len(miners) + 19
        left = 37
        d.add(left, top+0, WFrame(24, 5, "PROFIT / LOSS:"))
        d.add(left + 1, top+2, "daily cost")
        d.add(left + 1, top+3, "daily income")

        #d.add(left + 11, top+2, "$ " + str(price_btc))
        #d.add(left + 11, top+3, "$ " + str(price_sat)[0:9]) #only 8 chars

        # SIMULATE BUTTON
        b = WButton("SIMULATE")
        d.add(40, 1, b)
        b.finish_dialog = ACTION_SIMULATE

        # QUIT BUTTON
        b = WButton(" X ")
        d.add(FAT-3, 1, b)
        b.finish_dialog = ACTION_CANCEL

        res = d.loop()

    # QUIT BUTTON / or you push escape/Ctrl-C
    #if res == ACTION_OK or res == ACTION_CANCEL:
    if res == ACTION_CANCEL:
        return False # DON'T KEEP RUNNING

    if res == ACTION_SIMULATE:
        while True:
            if not dialog_simulate(): # stay in this modal until the user closes THAT window
                break

    if res == ACTION_ADDMINER:
        dialog_add_miner()

    if res == ACTION_REMOVEMINER:
        dialog_remove_miner()

    return True # RUN AGAIN
