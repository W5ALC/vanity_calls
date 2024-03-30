#!/usr/bin/env python

import csv

################################################################################

def chars(first, last):
    res = []
    for c in range(ord(first), ord(last)+1):
        res.append(chr(c))
    return res
    
def alphabet():
    return chars('A', 'Z')

def numbers():
    return chars('0', '9')

def two_by_one(remove_11_13=True):
    res = []
    for a in ['A', 'K', 'N', 'W']:
        for b in alphabet():
            for c in numbers():
                for d in alphabet():
                    if (a == 'A') and (ord(b) >= ord('M')):
                        # Any call sign having the letters AM-AZ as the prefix
                        # is assigned to other countries by the ITU.
                        continue
                    if (a+b in ['KP', 'NP', 'WP']) and (int(c) in [0, 6, 7, 8, 9]):
                        # Any 2-by-1 format call sign having the letters KP, NP
                        # or WP as the prefix and the numeral 0, 6, 7, 8 or 9
                        # is not available for assignment.
                        continue
                    if remove_11_13 and (a+b in ['AL', 'KL', 'NL', 'WL', 'KP', 'NP', 'WP', 'AH', 'KH', 'NH', 'WH']):
                        # Two letter prefixes that are designated for regions
                        # 11-13 are not available in regions 1-10.
                        continue
                    res.append(a+b+c+d)
    return res

def one_by_two():
    res = []
    for a in ['K', 'N', 'W']:
        for b in numbers():
            for c in alphabet():
                for d in alphabet():
                    res.append(a+b+c+d)
    return res

################################################################################

def group_callsigns(remaining):
    grouped_callsigns = {str(i): [] for i in range(10)}
    for callsign in remaining:
        for digit in range(10):
            if str(digit) in callsign:
                grouped_callsigns[str(digit)].append(callsign)
                break
    return grouped_callsigns

def print_grouped_callsigns(grouped_callsigns):
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

db = './HD.dat'

possibilities = one_by_two() + two_by_one()

in_use = []
with open(db) as csvfile:
    csvreader = csv.reader(csvfile, delimiter='|')
    for row in csvreader:
        if row[5] == 'A':  # Active, not Cancelled Expired or Terminated
            if len(row[4]) == 4:  # only care about 2x1 and 1x2
                in_use.append(row[4])

remaining = []
for callsign in possibilities:
    if callsign not in in_use:
        remaining.append(callsign)

grouped_callsigns = group_callsigns(remaining)
print_grouped_callsigns(grouped_callsigns)
print("Total remaining call signs:", len(remaining))
