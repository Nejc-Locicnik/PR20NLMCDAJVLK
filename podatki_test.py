import numpy as np
import matplotlib
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