import numpy as np
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

""" 
fajli:
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2015.csv
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2016.csv
- podatki/Parking_Violations_Issued_-_Fiscal_Year_2017.csv
"""

# zacetni dataset
dataset = pd.read_csv("podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014__small.csv", parse_dates=['Issue Date'])


def beri_dataset(filename):
    # branje in parsanje datumov v format datetime:
    dataset = pd.read_csv(filename, parse_dates=['Issue Date'])


def kazni_datum():
    """ GRAF ŠTEVILA KAZNI PO DATUMIH: """

    date_count = dataset.groupby(['Issue Date'])[['Issue Date']].agg('count')
    # dodajanje mankajočih datumov in jih fillat z ničlo:
    date_range = pd.date_range('03-01-2013', '09-01-2013')
    date_count = date_count.reindex(date_range, fill_value=0)
    # izris:
    plt.plot(date_count)
    plt.title("Število napisanih kazni 2013/2014")
    plt.xlabel('Datum')
    plt.xticks(rotation=90)
    plt.ylabel('Št. parkirnih kazni')
    plt.show()


def kazni_dan_v_tednu():
    """ KAZNI GLEDE NA DAN V TEDNU: """

    weekday_count = dataset.groupby(dataset['Issue Date'].dt.dayofweek).agg('count')['Issue Date']
    # izris:
    plt.bar(np.array(['mon','tue','wed','thu','fri','sat','sun']), weekday_count)
    plt.title("Kazni glede na dan v tednu 2013/2014")
    plt.xlabel('Dan v tednu')
    plt.ylabel('Skupno št. parkirnih kazni')
    plt.show()


def kazni_proizvajalec_abs():
    """ KAZNI GLEDE NA PROIZVAJALCA AVTOMOBILA (ABSOLUTNO) """

    # dataset2 = pd.read_csv("podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv", parse_dates=['Issue Date'])
    vehicle_make_count = dataset.groupby(['Vehicle Make'])['Vehicle Make'].agg('count')
    # sortarinje padajoče:
    vehicle_make_count = vehicle_make_count.sort_values(ascending=False)
    top_vehicle_make = vehicle_make_count.head(20)
    top_vehicle_make.plot.barh(top_vehicle_make)
    # izris:
    plt.title("Absolutno število kazni glede na proizvajalca avtomobila 2013/2014")
    plt.xlabel('Število kazni')
    plt.ylabel('Proizvajalec')
    plt.show()


def kazni_proizvajalec_rel():
    """ KAZNI GLEDE NA PROIZVAJALCA AVTOMOBILA (RELATIVNO) """

    vehicle_make_count_r = dataset.groupby(['Vehicle Make'])['Vehicle Make'].agg('count')
    # vehicle_make_count_r = vehicle_make_count_r.sort_values(ascending=False)
    vehicle_make_count_r = vehicle_make_count_r.sort_values(ascending=False)
    top_vehicle_make_r = vehicle_make_count_r.head(20)
    top_vehicle_make_r = top_vehicle_make_r.to_frame()
    # 2014 market share (https://www.goodcarbadcar.net/december-2014-usa-autosales-brand-results-rankings/)
    shares = np.array([
        14.4, # FORD
        12.1, # TOYOT
        8.3,  # HONDA
        12.3, # CHEVR
        7.7,  # NISSA
        3.5,  # DODGE
        3.0,  # GMC
        2.2,  # ME/BE
        1.0,  # FRUEH (Fruehauf)                - NO DATA
        1.0,  # INTER (International Harvester) - NO DATA
        2.1,  # BMW
        4.2,  # JEEP
        4.4,  # HYUND
        1.9,  # LEXUS
        1.0,  # ACURA
        2.2,  # VOLKS
        1.9,  # CHRYS
        0.6,  # LINCO
        0.5,  # MITSU
        0.7]  # INFIN
    )
    top_vehicle_make_r = top_vehicle_make_r.assign(share=shares)
    top_vehicle_make_r['Relative'] = top_vehicle_make_r['Vehicle Make'] / top_vehicle_make_r.share
    top_vehicle_make_r = top_vehicle_make_r.sort_values('Relative', ascending=False)
    print(top_vehicle_make_r)
    # izris:
    plt.barh(top_vehicle_make_r.index, top_vehicle_make_r['Relative'])
    plt.title("Relativno število kazni glede na proizvajalca avtomobila 2013/2014")
    plt.xlabel('Število kazni')
    plt.ylabel('Proizvajalec')
    plt.show()


beri_dataset("podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014__small.csv")
kazni_datum()
kazni_dan_v_tednu()
kazni_proizvajalec_abs()
kazni_proizvajalec_rel()
