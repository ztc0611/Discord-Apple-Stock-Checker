###This file is for testing, mostly.


import json
import urllib.request
import time
from datetime import datetime

def check_stock(url, id, file0, file1, file2, file3):

    response = urllib.request.urlopen(url+id)
    data = response.read()
    values = json.loads(data)

    try:
        print(id+","+values["body"]["content"]["pickupMessage"]["stores"][0]["country"]+","+str(values["body"]["content"]["pickupMessage"]["stores"][0]["storelongitude"])+","+str(values["body"]["content"]["pickupMessage"]["stores"][0]["storelatitude"]))
        file0.write(id+","+values["body"]["content"]["pickupMessage"]["stores"][0]["country"]+","+str(values["body"]["content"]["pickupMessage"]["stores"][0]["storelongitude"])+","+str(values["body"]["content"]["pickupMessage"]["stores"][0]["storelatitude"])+"\n")
        if values["body"]["content"]["pickupMessage"]["stores"][0]["country"] == "US":
            file3.write(id+"\n")
        else:
            file2.write(id+"\n")

        file1.write(str(values["body"]["content"]["pickupMessage"]["stores"][0]["storelongitude"])+","+str(values["body"]["content"]["pickupMessage"]["stores"][0]["storelatitude"])+"\n")
    except:
        print(id+",nothing")
        file2.write(id+"\n")
        file0.write(id+",nothing"+"\n")

url = "https://www.apple.com/shop/fulfillment-messages?parts.0=MK0U3LL/A&store=R"

check = open("data/all.txt", "r")
check2 = check.readlines()
id_num = len(check2)
print(id_num)
check.close()

f0 = open("data/all.txt", "a")
f1 = open("data/coords.txt", "a")
f2 = open("data/blacklist.txt", "a")
f3 = open("data/whitelist.txt", "a")

n = 800
for i in range(id_num, n+1):
    check_stock(url,f"{i:03}", f0, f1, f2, f3)
    time.sleep(3)

f0.close()
f1.close()
f2.close()
f3.close()