# https://www.techgig.com/practice/question/predict-housing-price/N3ZxRkJMWjhaanVZdkRpS0ZBTDFUbmk4cWtNRlV6cFI2UHI4NUJkWmtOWUR4VDhQejJEdDZUcUxpQmNGMTVULw==/1

from os import walk
import re

WORK_DIR = 'data/'
records = {
    'Locations': {}
}

start_year = 9999
location_set = set()
locations = 0


def extract_features(record):
    pass


def find_record(filename):
    f = open(WORK_DIR + filename)
    lines = f.readlines()
    f.close()
    global start_year

    e1 = re.compile("^House ID :\s+(.*)$")
    # Date Built : 2/10/1603 8:51 PM and Date Priced :  6/5/1611 11:44 PM
    e2 = re.compile("^Date Built\s*:\s*(\d{1,2})/(\d{1,2})/(\d{4})\D+(\d{1,2}:\d{1,2})\D+(\d{1,2})/(\d{1,2})/(\d{4})*.")
    e3 = re.compile("(\S+)\sgarden")
    # Distance from the Dock is 38.419444 holy lights
    e4 = re.compile("^Distance from the Dock is (\d+\.\d+)")
    # Distance from Capital is 0.256239 holy lights
    e5 = re.compile("^Distance from Capital is (\d+\.\d+)")
    # Distance from Royal Market is 69.486467 holy lights
    e6 = re.compile("^Distance from Royal Market is (\d+\.\d+)")
    # Distance from Guarding Tower is 14.394903 holy lights
    e7 = re.compile("^Distance from Guarding Tower is (\d+\.\d+)")
    # Distance from the River is 63.109038 holy lights
    e8 = re.compile("^Distance from the River is (\d+\.\d+)")
    # The house did not undergo renovation
    # The house underwent renovation upon Mighty King's command
    e9 = re.compile("(\S+)\srenovation")
    # There are 3 dining rooms
    e10 = re.compile("^There are (\d+) dining rooms$")
    # There are 4 bedrooms
    e11 = re.compile("^There are (\d+) bedrooms$")
    # King couldn't pay his visit to the house
    # The great King Visited this house once !
    e12 = re.compile("([Vv])isit")
    # Sorcerer couldn't curse this house
    # This house was cursed by sorcerer !!
    e13 = re.compile("([Ss])orcerer")
    # King blessed the house with 160 blessings
    e14 = re.compile("^King blessed the house with (\d+) blessings$")
    # There is a small land of farm in the front
    # There is no land of farm around
    e15 = re.compile("(\S+) land of farm")
    # Location of the house is : King's Landing
    e16 = re.compile("^Location of the house is : (.*)")
    # Holy tree stands tall beside the house
    # Holy tree was cut to death by Ancient Witch
    e17 = re.compile("^Holy tree (\S+)")
    # Distance from Knight's house is 10.505662 holy lights
    e18 = re.compile("^Distance from Knight's house is (\d+\.\d+)")
    # There are 4 bathrooms
    e19 = re.compile("^There are (\d+) bathrooms$")

    current_id = None
    for line in lines:
        result = e1.search(line)
        if result:
            current_id = result.group(1)
            continue
        result = e2.search(line)
        if result:
            m1, y1, m2, y2 = int(result.group(1)), int(result.group(3)), int(result.group(5)), int(result.group(7))
            if y1 < y2:
                if y1 < start_year:
                    start_year = y1
            elif y2 < start_year:
                start_year = y2
            records[current_id] = {
                'm1': m1,
                'y1': y1,
                'm2': m2,
                'y2': y2
            }
            continue

        result = e3.search(line)
        if result:
            if result.group(1) == 'for':
                records[current_id]['garden'] = 2
            elif result.group(1) == 'beautiful':
                records[current_id]['garden'] = 1
            else:
                print("ERROR: garden")
            continue

        result = e4.search(line)
        if result:
            records[current_id]['Dock'] = float(result.group(1))
            continue

        result = e5.search(line)
        if result:
            records[current_id]['Capital'] = float(result.group(1))
            continue

        result = e6.search(line)
        if result:
            records[current_id]['Royal Market'] = float(result.group(1))
            continue

        result = e7.search(line)
        if result:
            records[current_id]['Guarding Tower'] = float(result.group(1))
            continue

        result = e8.search(line)
        if result:
            records[current_id]['River'] = float(result.group(1))
            continue

        result = e9.search(line)
        if result:
            if result.group(1) == 'undergo':
                records[current_id]['renovation'] = 2
            else:
                records[current_id]['renovation'] = 1
            continue

        result = e10.search(line)
        if result:
            records[current_id]['dining rooms'] = float(result.group(1))
            continue

        result = e11.search(line)
        if result:
            records[current_id]['bedrooms'] = float(result.group(1))
            continue

        result = e12.search(line)
        if result:
            if result.group(1) == 'v':
                records[current_id]['visit'] = 2
            else:
                records[current_id]['visit'] = 1
            continue

        result = e13.search(line)
        if result:
            if result.group(1) == 'S':
                records[current_id]['curse'] = 1
            else:
                records[current_id]['curse'] = 2
            continue

        result = e14.search(line)
        if result:
            records[current_id]['blessings'] = float(result.group(1))
            continue

        result = e15.search(line)
        if result:
            if result.group(1) == 'no':
                records[current_id]['farm'] = 0
            elif result.group(1) == 'small':
                records[current_id]['farm'] = 1
            else:
                records[current_id]['farm'] = 2
            continue

        result = e16.search(line)
        if result:
            records['Locations']

            records[current_id]['Location'] = result.group(1)
            location_set.add(result.group(1))
            continue

        result = e17.search(line)
        if result:
            if result.group(1) == 'stands':
                records[current_id]['Holy tree'] = 1
            else:
                records[current_id]['Holy tree'] = 2
            continue

        result = e18.search(line)
        if result:
            records[current_id]['Knights house'] = float(result.group(1))
            continue

        result = e19.search(line)
        if result:
            records[current_id]['bathrooms'] = float(result.group(1))
            continue

        if line != '\n':
            print('** ', line)


f_list = []
for (dirpath, dirnames, filenames) in walk(WORK_DIR):
    f_list.extend(filenames)
    break

for f in f_list:
    x = re.search(".*txt$", f)
    if x:
        find_record(f)

f = open(WORK_DIR + 'house_prices.csv')
lines = f.readlines()
f.close()
del lines[0]
for line in lines:
    l = line.split(',')
    if l[0] == '':
        continue
    records[l[0]]['price'] = int(l[1])

print('6e32cec0: ', records['6e32cec0'])
