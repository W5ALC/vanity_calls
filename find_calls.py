#!/usr/bin/env python

import csv
import os
import requests
import zipfile
import shutil

# Define constants
ALPHABET_START = 'A'
ALPHABET_END = 'Z'
NUMBERS_START = '0'
NUMBERS_END = '9'

################################################################################

def generate_chars(start, end):
    """Generate a list of characters from start to end."""
    return [chr(c) for c in range(ord(start), ord(end) + 1)]

def alphabet():
    """Return the alphabet characters."""
    return generate_chars(ALPHABET_START, ALPHABET_END)

def numbers():
    """Return the numerical digits."""
    return generate_chars(NUMBERS_START, NUMBERS_END)

def two_by_one(remove_11_13=True):
    """Generate 2-by-1 format call signs."""
    res = []
    for a in ['A', 'K', 'N', 'W']:
        for b in alphabet():
            for c in numbers():
                for d in alphabet():
                    if (a == 'A') and (ord(b) >= ord('M')):
                        continue
                    if (a+b in ['KP', 'NP', 'WP']) and (int(c) in [0, 6, 7, 8, 9]):
                        continue
                    if remove_11_13 and (a+b in ['AL', 'KL', 'NL', 'WL', 'KP', 'NP', 'WP', 'AH', 'KH', 'NH', 'WH']):
                        continue
                    res.append(a+b+c+d)
    return res

def one_by_two():
    """Generate 1-by-2 format call signs."""
    res = []
    for a in ['K', 'N', 'W']:
        for b in numbers():
            for c in alphabet():
                for d in alphabet():
                    res.append(a+b+c+d)
    return res

################################################################################

def group_callsigns(remaining):
    """Group remaining callsigns by the last digit."""
    grouped_callsigns = {str(i): [] for i in range(10)}
    for callsign in remaining:
        for digit in range(10):
            if str(digit) in callsign:
                grouped_callsigns[str(digit)].append(callsign)
                break
    return grouped_callsigns

def print_grouped_callsigns(grouped_callsigns):
    """Print grouped callsigns."""
    max_column_width = max(len(callsigns) for callsigns in grouped_callsigns.values())
    columns = len(grouped_callsigns)
    for i in range(max_column_width):
        for j in range(columns):
            digit = str(j)
            callsigns = grouped_callsigns[digit]
            callsigns.sort()  # Sort call signs alphabetically
            if i < len(callsigns):
                print(f"{callsigns[i]:<8}", end="")
            else:
                print(" " * 8, end="")
        print()

def main():
    """Main function."""
    # Download and extract the ZIP file
    zip_url = 'https://data.fcc.gov/download/pub/uls/complete//l_amat.zip'
    zip_filename = 'l_amat.zip'
    extract_dir = 'extracted'
    csv_filename = 'HD.dat'

    print("Downloading and extracting the ZIP file...")
    response = requests.get(zip_url)
    with open(zip_filename, 'wb') as zip_file:
        zip_file.write(response.content)

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extract(csv_filename, extract_dir)

    os.remove(zip_filename)

    # Run the remaining part of the script
    db = os.path.join(extract_dir, csv_filename)

    # Generate all possible call signs
    possibilities = one_by_two() + two_by_one()

    # Get currently in-use call signs
    in_use = []
    with open(db) as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        for row in csvreader:
            if row[5] == 'A' and len(row[4]) == 4:  # Active and 2x1 or 1x2
                in_use.append(row[4])

    # Find remaining available call signs
    remaining = [callsign for callsign in possibilities if callsign not in in_use]

    # Group remaining call signs by the last digit
    grouped_callsigns = group_callsigns(remaining)

    # Print grouped call signs
    print_grouped_callsigns(grouped_callsigns)
    print("Total remaining call signs:", len(remaining))

    # Clean up extracted directory
    shutil.rmtree(extract_dir)

if __name__ == "__main__":
    main()
