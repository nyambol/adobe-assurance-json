# Extract Adobe Analytics data strings from Adobe Assurance (Project Griffon) logs
# 24 Oct 2022 11:18
# Michael Powe
# reminder of what we are looking for
# (json_data['events'][3]['payload']['ACPExtensionEventData']['hitUrl'])

import json
import urllib.parse
from argparse import ArgumentParser
from pprint import pprint


def main():
    # source data file
    griffon_data = r"c:\Users\micha\Dropbox\src\python\json\data\AssuranceTraining.json"

    # written output file
    url_data = r"c:\Users\micha\Dropbox\src\python\json\data\assurance-urls.txt"

    # list to collect matching URIs. It will then be written to file at the end
    uri_list = []
    # list to collect context data
    context_list = []

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="file from which to read")
    parser.add_argument("-o", "--output", help="file to which to write results")
    args = parser.parse_args()

    if args.file is not None:
        inputfile = args.file
    else:
        inputfile = griffon_data

    if args.output is not None:
        outputfile = args.output
    else:
        outputfile = url_data

    print("\n", inputfile, "\n")
    print(outputfile)

    f = open(griffon_data, "r")
    w = open(url_data, 'w')

    json_data = json.load(f)

    length = len(json_data['events'])

    for k in range(length):
        try:
            if 'hitUrl' in json_data['events'][k]['payload']['ACPExtensionEventData']:
                # remove the URI encoding and add to list for printing
                item = urllib.parse.unquote(json_data['events'][k]['payload']['ACPExtensionEventData'].get('hitUrl'))
                print(item)
                uri_list.append(item)
            elif 'contextdata' in json_data['events'][k]['payload']['ACPExtensionEventData']:
                item = json_data['events'][k]['payload']['ACPExtensionEventData'].get('contextdata')
                print("\n")
                pprint(item)
                print()
                context_list.append(item)
        except KeyError:
            print(">>>>>>>>>> <<<<<<<<<<")
            print(">>>>>>>>>> key error, `ACPExtensionEventData` not found <<<<<<<<<<")
            print(">>>>>>>>>> payload is ", json_data['events'][k]['payload'], "<<<<<<<<<<")
            print(">>>>>>>>>> <<<<<<<<<<")
    f.close()

    # output to file
    for i in uri_list:
        w.write(i + "\n")

    for i in context_list:
        w.write("\n")
        pprint(i, stream=w)

    w.close()

    # list of names
    # names = ['Jessa', 'Eric', 'Bob']
    #
    # with open(r'E:/demos/files_demos/account/sales.txt', 'w') as fp:
    #     fp.write("\n".join(str(item) for item in names))


if __name__ == "__main__":
    main()
