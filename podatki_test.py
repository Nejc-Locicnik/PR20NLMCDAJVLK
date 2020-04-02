import numpy as np
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt


def beri_dataset(filename):
    # branje in parsanje datumov v format datetime:
    return pd.read_csv(filename, parse_dates=['Issue Date'])


def kazni_datum():
    """ GRAF ŠTEVILA KAZNI PO DATUMIH: """

    date_count = dataset.groupby(['Issue Date'])[['Issue Date']].agg('count')
    # dodajanje mankajočih datumov in jih fillat z ničlo:
    date_range = pd.date_range('03-01-2013', '09-01-2013')
    date_count = date_count.reindex(date_range, fill_value=0)
    # izris:
    plt.rcParams.update({'figure.autolayout': True})
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
    plt.rcParams.update({'figure.autolayout': True})
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
    plt.rcParams.update({'figure.autolayout': True})
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
    plt.rcParams.update({'figure.autolayout': True})
    plt.barh(top_vehicle_make_r.index, top_vehicle_make_r['Relative'])
    plt.title("Relativno število kazni glede na proizvajalca avtomobila 2013/2014")
    plt.xlabel('Število kazni')
    plt.ylabel('Proizvajalec')
    plt.show()


kazne = {}
denar = {}
def preberi_kazne():
    tipKazne = pd.read_csv("podatki/DOF_Parking_Violation_Codes.csv")
    for i,j in zip(tipKazne["CODE"],tipKazne["DEFINITION"]):
        kazne[i] = j
    for i,j in zip(tipKazne["CODE"],tipKazne["All Other Areas"]):
        denar[i] = j


def najvec_kazni():
    """ KATERE KAZNE SO NAJPOGOSTEJSE """
    x = kazne.copy()
    for i in dataset["Violation Code"]:
        if i in kazne:
            try:
                x[i] += 1
            except:
                x[i] = 1
    najpogostejse = {}
    for i in x:
        if type(x[i]) == int:
            najpogostejse[i] = x[i]
    najpogostejse = {k: v for k, v in sorted(najpogostejse.items(), key=lambda item: item[1])}
    plt.rcParams.update({'figure.autolayout': True})
    plt.barh([kazne[i] for i in najpogostejse], list(najpogostejse.values()))
    plt.title("Število tipa kazni")
    plt.xlabel('Tip kazne')
    plt.ylabel('Število kazni')
    # plt.gcf().subplots_adjust(bottom=0.4)
    plt.show()


def stevilo_denarjaOdKazni():
    steviloDenara = 0
    print(denar)
    for i in dataset["Violation Code"]:
        if int(i) in denar.keys():
            steviloDenara += int(denar[i])
    print("Skupno število denarja pridobljenega od vseh kazni: {e}$".format(e=steviloDenara))


def kazni_leto():
    """ ŠT. KAZNI PO LETIH """

    st_kazni = [4716512+5821043, 5986831+5751009, 4872621+5368391]
    # info o prebivalcih dobil na https://worldpopulationreview.com/us-cities/new-york-city-population/
    prebivalci = [8398739, 8468181, 8475976]
    leta = ['2014', '2015', '2016']
    kazni__na_prebivalca = [k/p for k, p in zip(st_kazni, prebivalci)]

    # izris:
    plt.plot(leta, kazni__na_prebivalca)
    plt.title("Število parkirnih kazni na prebivalca")
    plt.ylabel('Št. kazni')
    plt.xlabel('Leto')
    plt.show()
    # spike leta 2015, mogoce kaksen razlog


# FULL DATASETS:
file_2014 = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014_.csv'
file_2015 = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2015.csv'
file_2016 = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2016.csv'
file_2017 = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2017.csv'

# SAMPLE DATASETS:
file_2014_small = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2014__August_2013___June_2014__small.csv'
file_2015_small = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2015_small.csv'
file_2016_small = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2016_small.csv'
file_2017_small = 'podatki/Parking_Violations_Issued_-_Fiscal_Year_2017_small.csv'

dataset = beri_dataset(file_2014_small)

kazni_datum()
kazni_dan_v_tednu()
kazni_proizvajalec_abs()
kazni_proizvajalec_rel()

preberi_kazne()
najvec_kazni()
stevilo_denarjaOdKazni()

kazni_leto()