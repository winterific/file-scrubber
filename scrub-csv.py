#!/usr/bin/python3
# -*- utf-8 -*-

import os
import sys
import csv
import re
import string
import random
import datetime
from datetime import date


def random_upper_letter(m):
    return random.choice(string.ascii_uppercase)


def random_lower_letter(m):
    return random.choice(string.ascii_lowercase)


def random_number(m):
    return random.choice(string.digits)


def random_punctuation(m):
    return random.choice(string.punctuation)


def random_date():
    earliest = datetime.date(1910,1,1)
    latest  = datetime.date(2018,1,1)
    delta = latest - earliest
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds    
    random_second = random.randrange(int_delta)
    return earliest + datetime.timedelta(seconds = random_second)


def scrub_text(text):
    text = re.sub(r'[A-Z]', random_upper_letter, text)
    text = re.sub(r'[a-z]', random_lower_letter, text)
    text = re.sub(r'[0-9]', random_number, text)
    # text = re.sub(r'[^a-z0-9\s]', random_punctuation, text, flags=re.IGNORECASE)
    return text


def scrub_field(column_name, text):
    # TODO: Make any special cases here, like finding out if the value is a date already and choosing a random valid date instead of gibberish, etc.
    # if text and re.search(r'date|dt', column_name, re.IGNORECASE):
    #     return random_date().strftime("%b/%d/%Y")
    return scrub_text(text)


def scrub_csv(input_filename, output_filename):
    with open(input_filename, 'r') as csv_input:
        with open(output_filename, 'w', newline='') as csv_output:
            reader = csv.DictReader(csv_input)
            writer = None
            writer = csv.DictWriter(csv_output, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                scrubbed_row={}
                for k,v in row.items():
                    scrubbed_row[k] = scrub_field(k,v)
                writer.writerow(scrubbed_row)


if __name__ == '__main__':
    n = len(sys.argv)
    if n <= 1:
        print("Input file name is required. e.g. ./scrub-csv.py file-input.csv")
        exit
    input_filename = sys.argv[1]
    if n > 2:
        output_filename = sys.argv[2]
    else:
        output_filename = os.path.splitext(input_filename)
        output_filename = output_filename[0] + '-scrubbed' + output_filename[1]
    # print(input_filename, output_filename)
    scrub_csv(input_filename, output_filename)