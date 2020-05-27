import numpy as np
import matplotlib
import pandas as pd
import geoplot as gplt
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


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

# tabela polnih imen znamk - po potrebi se lahko se dodajo
makes_full_names = np.flipud(np.array([
    ["MITSUBISHI", "MITSU"],
    ["MERCURY", "MERCU"],
    ["VOLKSWAGEN", "VOLKS"],
    ["MERCEDES-BENZ", "ME/BE"],
    ["INFINITI", "INFIN"],
    ["HYUNDAI", "HYUND"],
    ["NISSAN", "NISSA"],
    ["CHRYSLER", "CHRYS"],
    ["CHEVROLET", "CHEVR"],
    ["TOYOTA", "TOYOT"],
    ["LINCOLN", "LINCO"],
    ["INT. HARVESTER", "INTER"],
    ["FRUEHAUF", "FRUEH"]]))


def main():
    kazni_datum_group_teden()
    kazni_dan_v_tednu()
    kazni_proizvajalec_abs()
    kazni_proizvajalec_rel()  # pravilno delujoče zgolj za file_2014

    preberi_kazne()
    najvec_kazni()
    stevilo_denarjaOdKazni()

    kazni_leto_na_prebivalca()
    kazni_distrikt()

    # long_lat_to_csv(dataset, 'test.csv')

def beri_dataset(filename):
    """ BRANJE IN PARSANJE DATUMOV V DATETIME: """

    dataset = pd.DataFrame()
    # stolpci katere želimo brati:
    columns = [
        'Plate ID', 'Registration State', 'Issue Date',
        'Violation Code', 'Vehicle Body Type', 'Vehicle Make',
        'Issuing Agency', 'Vehicle Expiration Date', 'Violation Time',
        'Violation County', 'Violation In Front Of Or Opposite', 'Vehicle Color',
        'Unregistered Vehicle?', 'Vehicle Year', 'Street Name'
    ]

    print(columns)

    # optimizacija - ne beremo več celotnega dataseta v RAM hkrati (preprečitev memory errorjev)
    for chunk in pd.read_csv(filename, parse_dates=['Issue Date'], chunksize=1000000, usecols=columns,
                             dtype={"Violation County": str, 'Violation In Front Of Or Opposite': str}):
        dataset = pd.concat([dataset, chunk], ignore_index=True)
    return dataset


dataset = beri_dataset(file_2016_small)

def long_lat_to_csv(dataset, output_file):
    """ DODA LONGITUDE IN LATITUDE DATASETU TER EXPORTA V NOV CSV """
    
    print("function is on")
    # privzeta vrednost:
    dataset['longitude'] = None
    dataset['latitude'] = None
    geolocator = Nominatim(user_agent="test")
    longlat  = dict()
    area = "New York City, USA"
    for i, row in dataset.iterrows():
        if int(i) % 10 == 0:
            print('vrstica:', i)
        address = row['Street Name']
        try:
            # če je naslov že v slovarju:
            long, lat = longlat[address]
            dataset.at[i, 'longitude'] = long
            dataset.at[i, 'latitude'] = lat
        except:
            # če address še ni v slovarju:
            try:
                # z geolocatorjem dobi long in lat in naslov doda v slovar
                loc = geolocator.geocode(address + ',' + area)
                longlat[address] = [loc.longitude, loc.latitude]
            except:
                # da funkciji ni potrebno večkrat preverjat naslovou, ki vrnejo None
                longlat[address] = None
    
    out = './podatki/' + output_file
    dataset.to_csv(out, index=False)

def kazni_datum_group_teden():
    """ GRAF ŠTEVILA KAZNI PO DATUMIH: """

    date_count = dataset.groupby(dataset['Issue Date'])['Issue Date'].agg(['count'])
    # Issue date postane nazaj column in ne index:
    date_count = date_count.reset_index()
    # vsem datumom odštejemo 7 dni ker jih bomo groupirali, tako da bo group veljal za 7 dni naprej in ne 7 dni nazaj:
    date_count['Issue Date'] = pd.to_datetime(date_count['Issue Date']) - pd.to_timedelta(7, unit='d')
    # grupiramo vsak teden in seštejemo število kazni v tistem tednu:
    date_count = date_count.groupby([pd.Grouper(key='Issue Date', freq='W-MON')])['count'].sum().reset_index()
    # filtriranje datumov, ki ne bi smeli obstajati:
    date_count = date_count[(date_count['Issue Date'] > '2013-07-25') & (date_count['Issue Date'] < '2014-06-20')]
    # "Issue Date" nazaj v index dataframa:
    date_count = date_count.set_index('Issue Date')
    # izris:
    plt.rcParams.update({'figure.autolayout': True})
    plt.plot(date_count)
    plt.ylim(bottom=0)
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
    plt.bar(np.array(['pon', 'tor', 'sre', 'čet', 'pet', 'sob', 'ned']), weekday_count)
    plt.title("Kazni glede na dan v tednu 2013/2014")
    plt.xlabel('Dan v tednu')
    plt.ylabel('Skupno št. parkirnih kazni')
    plt.show()


def kazni_proizvajalec_abs():
    """ KAZNI GLEDE NA PROIZVAJALCA AVTOMOBILA (ABSOLUTNO) """

    vehicle_make_count = dataset.groupby(['Vehicle Make'])['Vehicle Make'].agg('count')
    # sortarinje padajoče:
    vehicle_make_count = vehicle_make_count.sort_values(ascending=False)
    top_vehicle_make = vehicle_make_count.head(20)

    # polna imena
    top_vehicle_make = top_vehicle_make.rename({b: a for a, b in makes_full_names})

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
        14.4,  # FORD
        12.1,  # TOYOT
        8.3,  # HONDA
        12.3,  # CHEVR
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

    # polna imena
    top_vehicle_make_r = top_vehicle_make_r.rename({b: a for a, b in makes_full_names})

    # izris:
    plt.rcParams.update({'figure.autolayout': True})

    plt.barh(top_vehicle_make_r.index, top_vehicle_make_r['Relative'])
    plt.title("Relativno število kazni glede na proizvajalca avtomobila 2013/2014")
    plt.xlabel('Število kazni')
    plt.ylabel('Proizvajalec')
    plt.show()


def trans(tip):
    # po potrebi se se lahko dodajo
    prevodi = {
        "NON-COMPLIANCE W/ POSTED SIGN": "Neupoštevanje znaka",
        "NO MATCH-PLATE/STICKER": "Neujemajoča tablica/nalepka",
        "NGHT PKG ON RESID STR-COMM VEH": "Nočno parkiranje - gosp. vozilo",
        "OBSTRUCTING TRAFFIC/INTERSECT": "Oviranje prometa/križišča",
        "NO STANDING-EXC. TRUCK LOADING": "Prepoved stojenja",
        "DOUBLE PARKING": "Dvojno parkiranje",
        "DOUBLE PARKING-MIDTOWN COMML": "Dvojno parkiranje - sredi mesta",
        "CROSSWALK": "Prehod za pešce",
        "NO STANDING-DAY/TIME LIMITS": "Prepovedano parkiranje",
        "NO STANDING-BUS STOP": "Prepoved stojenja - avtob. postaja",
        "BUS LANE VIOLATION": "Kršitev avtobusnega pasu",
        "FIRE HYDRANT": "Požarni hidrant",
        "FAIL TO DISP. MUNI METER RECPT": "Brez parkirnega listka",
        "FAILURE TO STOP AT RED LIGHT": "Neupoštevanje rdeče luči",
        "EXPIRED MUNI METER": "Potečen parkirni listek",
        "NO PARKING-DAY/TIME LIMITS": "Prepoved parkiranja",
        "INSP. STICKER-EXPIRED/MISSING": "Potečena ali manjkajoča nalepka",
        "PHTO SCHOOL ZN SPEED VIOLATION": "Omejena hitrost šolske cone",
        "FAIL TO DSPLY MUNI METER RECPT": "Brez parkirnega listka",
        "NO PARKING-STREET CLEANING": "Prepovedano parkiranje - čiščenje",
        "BIKE LANE": "Kolesarski pas",
        "FRONT OR BACK PLATE MISSING": "Manjkajoča tablica",
        "NO STANDING-COMM METER ZONE": "Prepovedano parkiranje",
        "REG. STICKER-EXPIRED/MISSING": "Potečena/manjkajoča reg. nalepka"
    }
    if tip in prevodi:
        tip = prevodi[tip]
    return tip


kazne = {}
denar = {}


def preberi_kazne():
    tipKazne = pd.read_csv("podatki/DOF_Parking_Violation_Codes.csv")
    for i, j in zip(tipKazne["CODE"], tipKazne["DEFINITION"]):
        kazne[i] = trans(j) # klice se prevod
    for i, j in zip(tipKazne["CODE"], tipKazne["All Other Areas"]):
        denar[i] = j


def najvec_kazni():
    """ KATERE KAZNE SO NAJPOGOSTEJSE """
    x = kazne.copy()
    for i in dataset["Violation Code"]:
        if i in kazne:
            # kodi 38 in 69 predstavljata enak prekršek
            if i == 38:
                i = 69
            try:
                x[i] += 1
            except:
                x[i] = 1
    najpogostejse = []
    for i in x:
        if type(x[i]) == int:
            najpogostejse.append((x[i], i))
    plt.rcParams.update({'figure.autolayout': True})
    plt.barh([kazne[j] for i, j in sorted(najpogostejse, reverse=True)[:20]],
             [i for i, j in sorted(najpogostejse, reverse=True)[:20]])
    plt.title("Število tipa kazni")
    plt.ylabel('Tip kazni')
    plt.xlabel('Število kazni')
    # plt.xticks(rotation=90)
    # plt.gcf().subplots_adjust(bottom=0.4)
    plt.show()


def stevilo_denarjaOdKazni():
    steviloDenara = 0
    for i in dataset["Violation Code"]:
        if int(i) in denar.keys():
            steviloDenara += int(denar[i])
    print("Skupno število denarja pridobljenega od vseh kazni: {e}$".format(e=steviloDenara))


def kazni_leto_na_prebivalca():
    """ ŠT. KAZNI PO LETIH """

    # izracunano za dejanska leta 2014, 2015 in 2016
    st_kazni = [4716512 + 5821043, 5986831 + 5751009, 4872621 + 5368391]
    # info o prebivalcih dobil na https://worldpopulationreview.com/us-cities/new-york-city-population/
    prebivalci = [8398739, 8468181, 8475976]
    leta = ['2014', '2015', '2016']
    kazni_na_prebivalca = [k / p for k, p in zip(st_kazni, prebivalci)]

    # izris:
    plt.plot(leta, kazni_na_prebivalca)
    plt.title("Število parkirnih kazni na prebivalca")
    plt.ylabel('Št. kazni')
    plt.xlabel('Leto')
    plt.show()
    # spike leta 2015, mogoce kaksen razlog


def kazni_distrikt():
    """ Demografika NYC: https://en.wikipedia.org/wiki/Demographics_of_New_York_City
    - Ni tocnih podatkov za vsako leto, vzamem avg 2010 in 2019

    - Staten Island:
    # 2010 - 468,730
    # 2019 - 476,143

    - Bronx:
    # 2010 - 1,385,108
    # 2019 - 1,418,207

    - Queens:
    # 2010 - 2,230,722
    # 2019 - 2,253,858

    - Brooklyn:
    # 2010 - 2,504,700
    # 2019 - 2,559,903

    - Manhattan:
    # 2010 - 1,585,873
    # 2019 - 1,628,706  """

    """ funkcije za izracun kazni v distriktih """
    # streets = dataset[(dataset['Issue Date'] > '2016-01-01 00:30:00')&(dataset['Issue Date'] < '2016-12-31 00:30:00')]
    # streets = streets.groupby(['Violation County'])['Violation County'].agg('count')

    districts = ['Staten Island', 'Bronx', 'Queens', 'Brooklyn', 'Manhattan']
    pop_district = [944873, 2803315, 4484580, 5064603, 3214579]

    leta = ['2014', '2015', '2016']
    kazni_2014 = [59714 + 62429,  504189 + 580031, 953598 + 1024853, 1016539 + 1158171, 1846962 + 1975193]
    kazni_2015 = [51856 + 53971,  602852 + 582918, 1139422 + 1009489, 1236619 + 1190294, 2133928 + 1853098]
    kazni_2016 = [50195 + 130140, 495769 + 672460, 886512 + 1261145, 1088374 + 1589315, 1694160 + 1693039]

    kazni_pop = []

    for kazni in [kazni_2014, kazni_2015, kazni_2016]:
        kazni_leto = []
        for ime, kazni, pop in zip(districts, kazni, pop_district):
            kazni_leto.append(kazni/pop)
        kazni_pop.append(kazni_leto)

    kazni_pop.reverse()
    # izris:
    legend=[]
    for j in reversed(range(5)):  # vsak distrikt
        l, = plt.plot(leta, [kazni_pop[i][j] for i in range(3)], label=districts[j], linewidth=3.0)    # vsako leto
        legend.append(l)
    plt.legend(handles=legend, bbox_to_anchor=(0.8, 0.45))

    plt.title("Število parkirnih kazni na prebivalca za posamezen distrikt")
    plt.ylabel('Št. kazni na preb.')
    plt.xlabel('Leto')
    plt.show()


main()
""" 2014 <- file_2014
#       BRONX           504189
#       BROOKLYN        1016539
#       MANHATTAN       1846962
#       QUEENS          953598
#       STATEN ISLAND   59714
"""
"""     2014 <- file_2015
#       BRONX           580031
#       BROOKLYN        1158171
#       MANHATTAN       1975193
#       QUEENS          1024853
#       STATEN ISLAND   62429
"""
"""     2015 <- file_2015
#       BRONX           602852
#       BROOKLYN        1236619
#       MANHATTAN       2133928
#       QUEENS          1139422
#       STATEN ISLAND   51856
"""
"""
#   2015 <- file_2016
#       BRONX           582918
#       BROOKLYN        1190294
#       MANHATTAN       1853098
#       QUEENS          1009489
#       STATEN ISLAND   53971
"""

"""
#   2016 <- file_2016
#       BRONX           495769
#       BROOKLYN        1088374
#       MANHATTAN       1694160
#       QUEENS          886512
#       STATEN ISLAND   50195
"""

"""
Violation County

BX        495769

K        1006044 + 82330

NY       1684424 + 9736

Q         825206 + 61306

ST         10401 + 39794
"""

"""
#   2016 <- file_2017
#       BRONX           672460
#       BROOKLYN        1589315
#       MANHATTAN       1693039
#       QUEENS          1261145
#       STATEN ISLAND   130140
"""
