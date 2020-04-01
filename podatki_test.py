import numpy as np
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from csv import DictReader

""" 
fajli:
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2015.csv
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2016.csv
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2017.csv
"""

fp = open('podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014__small.csv', 'rt')
reader = DictReader(fp)

# ni normalizirano
vehicle_body_types = {}
vehicle_colors = {}
vehicle_makes = {}

for row in reader:

    vbt = row["Vehicle Body Type"]
    if vbt not in vehicle_body_types:
        vehicle_body_types[vbt] = 1
    else:
        vehicle_body_types[vbt] += 1

    vc = row["Vehicle Color"]
    if vc not in vehicle_colors:
        vehicle_colors[vc] = 1
    else:
        vehicle_colors[vc] += 1

    vm = row["Vehicle Make"]
    if vm not in vehicle_makes:
        vehicle_makes[vm] = 1
    else:
        vehicle_makes[vm] += 1


plt.figure(figsize=(10, 5))
plt.bar(vehicle_body_types.keys(), vehicle_body_types.values(), align="center", width=0.5, alpha=0.7)
plt.suptitle("Parkirne kazni gleda na tip vozila", size=18)
plt.xlabel('Tip vozila')
plt.ylabel('Št. parkirnih kazni')
plt.show()

print(vehicle_colors)
print(vehicle_makes)
print(vehicle_body_types)

# branje in parsanje datumov v format datetime: 
dataset = pd.read_csv("podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014__small.csv", parse_dates=['Issue Date'])

# GRAF ŠTEVILA KAZNI PO DATUMIH:

date_count = dataset.groupby(['Issue Date'])[['Issue Date']].agg('count')
# dodajanje mankajočih datumov in jih fillat z ničlo:
date_range = pd.date_range('03-01-2013', '09-01-2013')
date_count = date_count.reindex(date_range, fill_value=0)
# izris:
plt.plot(date_count)
plt.title("Število napisanih kazni 2013/2014", size=18)
plt.xlabel('Datum')
plt.xticks(rotation=90)
plt.ylabel('Št. parkirnih kazni')
plt.show()

# KAZNI GLEDE NA DAN V TEDNU:

weekday_count = dataset.groupby(dataset['Issue Date'].dt.dayofweek).agg('count')['Issue Date']
# izris:
plt.bar(np.array(['mon','tue','wed','thu','fri','sat','sun']), weekday_count)
plt.title("Kazni glede na dan v tednu 2013/2014", size=18)
plt.xlabel('Dan v tednu')
plt.ylabel('Skupno št. parkirnih kazni')
plt.show()

# KAZNI GLEDE NA PROIZVAJALCA AVTOMOBILA

# dataset2 = pd.read_csv("podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv", parse_dates=['Issue Date'])
vehicle_make_count = dataset.groupby(['Vehicle Make'])['Vehicle Make'].agg('count')
# sortarinje padajoče:
vehicle_make_count = vehicle_make_count.sort_values(ascending=False)
vehicle_make_count.head(20).plot.barh()
plt.title("Absolutno število kazni glede na proizvajalca avtomobila 2013/2014", size=18)
plt.xlabel('Število kazni')
plt.ylabel('Proizvajalec')
plt.show()