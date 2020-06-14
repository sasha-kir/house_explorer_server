import os
import csv

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def find_type_link(input_type):
    if input_type == "-":
        return ""

    with open(f"{DIR_PATH}/house_types.csv", "r", encoding="utf-8") as fin:
        csv_reader = csv.reader(fin, delimiter=";")
        for house_type, link in csv_reader:
            if input_type in house_type:
                return link

        return ""
