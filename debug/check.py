###This file is for testing, mostly.


import json
import urllib.request
import time
from datetime import datetime

def check_stock(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    values = json.loads(data)

    states = {}

    for i in values["body"]["content"]["pickupMessage"]["stores"]:
        
        if not i["state"] in states:
            states[i["state"]] = []
        states[i["state"]].append(i['storeName']+", "+i['city'])

        print(states)


        #if i["state"] != prev_state:
        #    print("\n"+i["state"])
        #    prev_state = i["state"]
        #print(i['storeName']+", "+i['city'])
        #for j in i["partsAvailability"]:
            #name = i["partsAvailability"][j]["storePickupProductTitle"]
            #name = name.replace("Studio Display", "")
            #name = name.replace(" - ", " ")
            #if i["partsAvailability"][j]["pickupDisplay"] == "available":
                #print(i['storeName'], ",", i['city'])
                #print("!!!!! ",name,":",i["partsAvailability"][j]["pickupDisplay"],"\n")
    #print(states)
    return states

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

url = "https://www.apple.com/shop/fulfillment-messages?parts.0=MK0U3LL/A&parts.1=MK0Q3LL/A&parts.2=MMYQ3LL/A&parts.3=MMYW3LL/A&parts.4=MMYV3LL/A&parts.5=MMYX3LL/A&store=R"

stores = []

check = open("data/whitelist.txt", "r")
stores = check.read().splitlines()
print(stores)

lastchecktime = 0
http_error = False

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

while True:

    all_stores = {}

    if int( time.time() ) > ((lastchecktime + 10*60) - 30):
        print(get_time(), "Checking inventory")
        for i in range(len(stores)):
            print(stores[i])
            new = check_stock(url+stores[i])
            all_stores = merge_two_dicts(all_stores, new)
            if i % 5 == 0 and i != 0:
                time.sleep(12.5)

        sorted_dict = {key: value for key, value in sorted(all_stores.items())}
        for i in sorted_dict:
            print("\n"+i)
            for j in sorted_dict[i]:
                print(j)

        print(get_time(), "Check finished")

        lastchecktime = int( time.time() )
    else:
        time.sleep(30)