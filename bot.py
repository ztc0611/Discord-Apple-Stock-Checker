url = "https://www.apple.com/shop/fulfillment-messages?parts.0=MK0U3LL/A&parts.1=MK0Q3LL/A&parts.2=MMYQ3LL/A&parts.3=MMYW3LL/A&parts.4=MMYV3LL/A&parts.5=MMYX3LL/A&store=R"

check = open("data/whitelist.txt", "r")
stores = check.read().splitlines()

import json
import urllib.request
import time
from datetime import datetime

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

#Checking stock function.
def check_stock(url, c):
    try:
        response = urllib.request.urlopen(url) #Get json from URL
        data = response.read()
        values = json.loads(data) #Convert

        in_stock = []

        for i in values["body"]["content"]["pickupMessage"]["stores"]:
            message = "["+i["storeNumber"]+"] Checking "+i["storeName"]+", "+i["city"]+", "+i["state"]
            #print(i['storeName']+", "+i['city']+", "+i["state"])
            for j in i["partsAvailability"]:
                name = i["partsAvailability"][j]["storePickupProductTitle"]
                if i["partsAvailability"][j]["pickupDisplay"] == "available":
                    in_stock.append({"name":name, "city":i['city'], "store_name":i['storeName'], "storeNumber":i["storeNumber"],"pickupDisplay":i["partsAvailability"][j]["pickupDisplay"], "state":i["state"]})
                    #print(i['storeName'], ",", i['city'])
                    #print("!!!!! ",name,":",i["partsAvailability"][j]["pickupDisplay"],"\n")
        return [in_stock,message]
    except Exception as e: 
        #print(e)
        time.sleep(10)
        #print("Retrying...")
        return check_stock(url, c)

####DISCORD BOT

def get_channel_id(d): #Get one of the six channels to post the update in

    n = d["name"]

    if n == "Studio Display - Standard glass - Tilt-adjustable stand":
        return 967521963952177222
    elif n == "Studio Display - Standard glass - Tilt- and height-adjustable stand":
        return 967521999792504922
    elif n == "Studio Display - Standard glass - VESA mount adapter":
        return 967522033556656239
    elif n == "Studio Display - Nano-texture glass - Tilt-adjustable stand":
        return 967522053102129213
    elif n == "Studio Display - Nano-texture glass - Tilt- and height-adjustable stand":
        return 967522081350770778
    elif n == "Studio Display - Nano-texture glass - VESA mount adapter":
        return 967522105363161108

import discord
from discord.ext import tasks
import time

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    #life_check.start()
    inv_check.start()

#Useful for debugging if the bot has crashed without console access as Discord's online indicator does not work well for bots.
#@tasks.loop(minutes=5)
#async def life_check():
    #channel = client.get_channel(967567108877725736)
    #await channel.send("I live.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

@tasks.loop(minutes=30)
async def inv_check():
    channel = client.get_channel(967567108877725736)
    await channel.send("Checking inventory.")
    print(get_time(), "Checking inventory.")
    for i in range(len(stores)):
        result = check_stock(url+stores[i], channel)
        message = result[1]
        result = result[0]
        if result == None:
            print(get_time(), "HTTP Error")
            break
        else:
            for j in result:
                alert_stream = client.get_channel(get_channel_id(j))
                message = "Model found at **"+j["store_name"]+", "+j["city"]+", "+j["state"]+"**!"
                await alert_stream.send(message)
        
        if i != 0:
            if len(stores) / i == 2:
                await channel.send("Check 50% Complete.")
                print(get_time(), "Check 50% Complete.")

            if i % 10 == 0:
                time.sleep(4)
    
    await channel.send("Check finished.")
    print(get_time(), "Check finished.")

import os
import sys
with open(os.path.join(sys.path[0], "token.txt"), "r") as f:
    token = f.read()
    f.close()
client.run(token) #Bot ID from file goes here.

### END DISCORD BOT