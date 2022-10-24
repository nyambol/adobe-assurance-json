# Extract Adobe Analytics data strings from Adobe Assurance (Project Griffon) logs
# 24 Oct 2022 11:18
# Michael Powe

import json
import urllib.parse

# from pprint import pprint

# (json_data['events'][3]['payload']['ACPExtensionEventData']['hitUrl'])

GRIFFON_DATA = r"c:\Users\micha\Dropbox\src\python\json\data\AssuranceTraining.json"
URL_DATA = r"c:\Users\micha\Dropbox\src\python\json\data\assurance-urls.txt"
DATA_LIST = []

f = open(GRIFFON_DATA, "r")
w = open(URL_DATA, 'w')
json_data = json.load(f)

length = len(json_data['events']) - 1

for k in range(length):
    try:
        if 'hitUrl' in json_data['events'][k]['payload']['ACPExtensionEventData']:
            item = urllib.parse.unquote(json_data['events'][k]['payload']['ACPExtensionEventData'].get('hitUrl'))
            print(item)
            DATA_LIST.append(item)
    except KeyError:
        print(">>>>>>>>>> <<<<<<<<<<")
        print(">>>>>>>>>> key error, `ACPExtensionEventData` not found <<<<<<<<<<")
        print(">>>>>>>>>>", json_data['events'][k]['payload'], "<<<<<<<<<<")
        print(">>>>>>>>>> <<<<<<<<<<")
f.close()

for i in DATA_LIST:
    w.write(i + "\n")

w.close()
