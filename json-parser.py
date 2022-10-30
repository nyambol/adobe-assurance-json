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
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="file from which to read")
    parser.add_argument("-o", "--output", help="file to which to write results")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print output to screen as well as to file",
    )
    args = parser.parse_args()

    # source data file (default if no command line input)
    griffon_data: str = (
        r"c:\Users\micha\Dropbox\src\python\json\data\AssuranceTraining.json"
    )

    # written output file (default if no command line input)
    url_data: str = r"c:\Users\micha\Dropbox\src\python\json\data\assurance-urls.txt"

    inputfile: str = args.file if args.file is not None else griffon_data
    outputfile: str = args.output if args.output is not None else url_data

    context_list: list[str]
    uri_list: list[str]
    uri_list, context_list = process_file(inputfile, pfarg=args.verbose)

    write_data(outputfile, uri_list, context_list)


def process_file(infile: str, pfarg: bool = None) -> tuple[list[str], list[str]]:
    """
    Processes the file of JSON generated by Adobe Assurance and collects the
    URI data string and the variable context data.

    :rtype: object
    :param arg: True to print to screen, default is False.
                Will be set True by the presence of the `-v` command line option
    :type arg: bool
    :param infile: Complete path and filename for the file to be processed
    :type infile: str
    """
    pfarg: bool = True if pfarg is not None and pfarg is not False else False

    f = open(infile, "r")

    # list to collect matching URIs. It will then be written to file at the end
    uri_list: list[str] = []
    # list to collect context data
    context_list: list[str] = []

    json_data: str = json.load(f)

    length: int = len(json_data["events"])

    for k in range(length):
        try:
            # this is what we use for validating data is correct
            if "hitUrl" in json_data["events"][k]["payload"]["ACPExtensionEventData"]:
                # remove the URI encoding and add to list for printing
                item: str = urllib.parse.unquote(
                    json_data["events"][k]["payload"]["ACPExtensionEventData"].get(
                        "hitUrl"
                    )
                )
                if pfarg:
                    print(item, "\n")
                uri_list.append(item)
            # this is what we use for validating context data variables (for SDR, &c)
            elif (
                "contextdata"
                in json_data["events"][k]["payload"]["ACPExtensionEventData"]
            ):
                item = (json_data["events"][k]["payload"]["ACPExtensionEventData"]).get(
                    "contextdata"
                )
                if pfarg:
                    print()
                    pprint(item)
                    print()
                context_list.append(item)
        # 'key' refers to dictionary key, not a keyboard key
        except KeyError:
            print(">>>>>>>>>> <<<<<<<<<<")
            print(">>>>>>>>>> key error, `ACPExtensionEventData` not found <<<<<<<<<<")
            print(
                ">>>>>>>>>> payload is ",
                json_data["events"][k]["payload"],
                "<<<<<<<<<<",
            )
            print(">>>>>>>>>> <<<<<<<<<<\n")
    f.close()
    return uri_list, context_list


def write_data(url_data: str, uri_list: list[str], context_list: list[str]) -> None:
    """
    Writes the accumulated URI and context data to a file. URI is written to
    the top of the file and context data follows it.

    :param uri_list: list in which data URI are captured from `hitUrl`
    :type uri_list: list
    :param context_list: list in which context data objects are captured
           from `contextdata`
    :type context_list: list
    :param url_data: the JSON file from which the data is to be extracted.
    :type url_data: str
    """
    w = open(url_data, "w")

    # output to file
    for i in uri_list:
        w.write(i + "\n")

    for i in context_list:
        w.write("\n")
        pprint(i, stream=w)

    w.close()


if __name__ == "__main__":
    main()
