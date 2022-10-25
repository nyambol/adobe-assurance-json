# Extract Adobe Analytics data strings from Adobe Assurance (Project Griffon) logs
# 24 Oct 2022 11:18
# Michael Powe
# reminder of what we are looking for
# (json_data['events'][3]['payload']['ACPExtensionEventData']['hitUrl'])

import json
import urllib.parse
from argparse import ArgumentParser
from pprint import pprint
from typing import List, Any


def process_file(infile, arg=None):
    if arg is not None and arg is not False:
        arg: bool = True

    f = open(infile, "r")

    # list to collect matching URIs. It will then be written to file at the end
    uri_list = []

    # list to collect context data
    context_list: list[str] = []

    json_data = json.load(f)

    length = len(json_data['events'])

    for k in range(length):
        try:
            # this is what we use for validating data is correct
            if 'hitUrl' in json_data['events'][k]['payload']['ACPExtensionEventData']:
                # remove the URI encoding and add to list for printing
                item = urllib.parse.unquote(json_data['events'][k]['payload']['ACPExtensionEventData'].get('hitUrl'))
                if arg:
                    print(item, "\n")
                uri_list.append(item)
            # this is what we use for validating context data variables (for SDR, &c)
            elif 'contextdata' in json_data['events'][k]['payload']['ACPExtensionEventData']:
                item = json_data['events'][k]['payload']['ACPExtensionEventData'].get('contextdata')
                if arg:
                    print()
                    pprint(item)
                    print()
                context_list.append(item)
        # 'key' refers to dictionary key, not a keyboard key
        except KeyError:
            print(">>>>>>>>>> <<<<<<<<<<")
            print(">>>>>>>>>> key error, `ACPExtensionEventData` not found <<<<<<<<<<")
            print(">>>>>>>>>> payload is ", json_data['events'][k]['payload'], "<<<<<<<<<<")
            print(">>>>>>>>>> <<<<<<<<<<\n")
    f.close()
    return uri_list, context_list


def write_data(url_data, uri_list, context_list):
    w = open(url_data, 'w')

    # output to file
    for i in uri_list:
        w.write(i + "\n")

    for i in context_list:
        w.write("\n")
        pprint(i, stream=w)

    w.close()


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="file from which to read")
    parser.add_argument("-o", "--output", help="file to which to write results")
    parser.add_argument("-v", "--verbose", action="store_true", help="print output to screen as well as to file")
    args = parser.parse_args()

    # source data file (default if no command line input)
    griffon_data = r"c:\Users\micha\Dropbox\src\python\json\data\AssuranceTraining.json"

    # written output file (default if no command line input)
    url_data = r"c:\Users\micha\Dropbox\src\python\json\data\assurance-urls.txt"

    inputfile = args.file if args.file is not None else griffon_data
    outputfile = args.output if args.output is not None else url_data

    uri_list, context_list = process_file(griffon_data, arg=args.verbose)

    write_data(url_data, uri_list, context_list)


if __name__ == "__main__":
    main()
