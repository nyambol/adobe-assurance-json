# Extract Adobe Analytics data strings from Adobe Assurance (Project Griffon) logs
# 24 Oct 2022 11:18
# Michael Powe

import json
import urllib.parse

# from pprint import pprint

# reminder of what we are looking for
# (json_data['events'][3]['payload']['ACPExtensionEventData']['hitUrl'])

# source data file
GRIFFON_DATA = r"c:\Users\micha\Dropbox\src\python\json\data\AssuranceTraining.json"

# written output file
URL_DATA = r"c:\Users\micha\Dropbox\src\python\json\data\assurance-urls.txt"

# list to collect matching URIs. It will then be written to file at the end
DATA_LIST = []

f = open(GRIFFON_DATA, "r")
w = open(URL_DATA, 'w')

json_data = json.load(f)

length = len(json_data['events'])

for k in range(length):
    try:
        if 'hitUrl' in json_data['events'][k]['payload']['ACPExtensionEventData']:
            # remove the URI encoding and add to list for printing
            item = urllib.parse.unquote(json_data['events'][k]['payload']['ACPExtensionEventData'].get('hitUrl'))
            print(item)
            DATA_LIST.append(item)
    except KeyError:
        print(">>>>>>>>>> <<<<<<<<<<")
        print(">>>>>>>>>> key error, `ACPExtensionEventData` not found <<<<<<<<<<")
        print(">>>>>>>>>> payload is ", json_data['events'][k]['payload'], "<<<<<<<<<<")
        print(">>>>>>>>>> <<<<<<<<<<")
f.close()

# output to file
for i in DATA_LIST:
    w.write(i + "\n")

w.close()
