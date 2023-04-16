
price_btc = 123456789
price_sat = 0.123456789


###############################################
###############################################
# ADD HERE
###############################################
miners=[]

miners.append({"name":"S9",
               "wattage":1400,
               "eff":78,
               "quantity":4
               })


###############################################
###############################################
# ADD HERE
###############################################
def total_wattage():
    t = 0
    for m in miners:
        t += m["wattage"] * m["quantity"]
    return t

###############################################
def total_hr():
    t = 0
    for m in miners:
        t += (m["wattage"] / m["eff"]) * m["quantity"]
    return t

###############################################
def total_eff():
    # avoid divide by zero when no miner list is empty
    if not len(miners): return 0

    e = 0
    for m in miners:
        e += m["eff"]
    return e / len(miners)
