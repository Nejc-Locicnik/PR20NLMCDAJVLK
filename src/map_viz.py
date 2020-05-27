import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from csv import DictReader

def razvrsti(county_code):
    bronx = {'BX', 'BRONX'}
    queens = {'Q', 'QUEEN', 'QU', 'QN', 'QNS'}
    brooklyn = {'BK', 'K', 'KINGS', 'KING'}
    staten_island = {'RICH', 'R', 'RC', 'ST'}
    manhattan = {'NYC', 'NY', 'NEWY', 'MH', 'NEW Y', 'MAN', 'MN'}
    if county_code in bronx:
        return 'Bronx'
    elif county_code in queens:
        return 'Queens'
    elif county_code in brooklyn:
        return 'Brooklyn'
    elif county_code in staten_island:
        return 'StatenIsland'
    elif county_code in manhattan:
        return 'Manhattan'
    else:
        return ""

def fill():
  reader = DictReader(open("podatki/Parking_Violations_Issued_-_Fiscal_Year_2017.csv", 'rt', encoding="utf-8"))
  
  kazni = {'solska_cona': {'Bronx': 0, 'StatenIsland': 0, 'Brooklyn': 0, 'Queens': 0, 'Manhattan': 0},
         'rdeca_luc': {'Bronx': 0, 'StatenIsland': 0, 'Brooklyn': 0, 'Queens': 0, 'Manhattan': 0},
         'nalepka': {'Bronx': 0, 'StatenIsland': 0, 'Brooklyn': 0, 'Queens': 0, 'Manhattan': 0},
         'listek': {'Bronx': 0, 'StatenIsland': 0, 'Brooklyn': 0, 'Queens': 0, 'Manhattan': 0},
         'prepoved_park': {'Bronx': 0, 'StatenIsland': 0, 'Brooklyn': 0, 'Queens': 0, 'Manhattan': 0},
         'ciscenje': {'Bronx': 0, 'StatenIsland': 0, 'Brooklyn': 0, 'Queens': 0, 'Manhattan': 0}}
  
  for row in reader:
    county = row["Violation County"]
    kazen = row["Violation Code"]
    county = razvrsti(county)
    if county != "":
        if kazen == '69' or kazen == '38':
            kazni['listek'][county] += 1
        elif kazen == '36':
            print("something")
            kazni['solska_cona'][county] += 1
        elif kazen == '7':
            kazni['rdeca_luc'][county] += 1
        elif kazen == '46':
            # dvojno parkiranje
            pass
        elif kazen == '71':
            kazni['nalepka'][county] += 1
        elif kazen == '31':
            kazni['prepoved_park'][county] += 1
        elif kazen == '21':
            kazni['ciscenje'][county] += 1
        else:
            pass
  return kazni

csv_2013_2014 = "podatki/2013_2014_test.csv"
csv_2015 = "podatki/2015_test.csv"
csv_2016 = "podatki/2016_test.csv"
csv_2017 = "podatki/2017_test.csv"

def draw_multiple_maps(file_csv):
  data = pd.read_csv(file_csv, header=0)
  shape = gpd.read_file("podatki/shape_boroughs/nybb.shp")
  merged = shape.set_index('BoroName').join(data.set_index('Borough'))  # rename Name

  fig, ax = plt.subplots(3, 3, figsize=(12, 12), dpi=150)
  fig.subplots_adjust(top=0.9, bottom=0.1, hspace=0.35)
  merged.plot(column='solska_cona', cmap='OrRd', linewidth=0.8, ax=ax[0][0], edgecolor='0.8')
  merged.plot(column='rdeca_luc', cmap='OrRd', linewidth=0.8, ax=ax[0][1], edgecolor='0.8')
  merged.plot(column='nalepka', cmap='OrRd', linewidth=0.8, ax=ax[0][2], edgecolor='0.8')
  merged.plot(column='listek', cmap='OrRd', linewidth=0.8, ax=ax[1][0], edgecolor='0.8')
  merged.plot(column='prepoved_park', cmap='OrRd', linewidth=0.8, ax=ax[1][1], edgecolor='0.8')
  merged.plot(column='ciscenje', cmap='OrRd', linewidth=0.8, ax=ax[1][2], edgecolor='0.8')

  sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=0, vmax=1))
  plt.colorbar(sm, ax=ax[2, :], location='top', pad=0.3, shrink=0.5)

  fig.suptitle("Leto 2015", fontsize=16)
  ax[0][0].axis('off')
  ax[0][0].set_title("Omejena hitrost šolske cone")
  ax[0][1].axis('off')
  ax[0][1].set_title("Neupoštevanje rdeče luči")
  ax[0][2].axis('off')
  ax[0][2].set_title("Potečena ali manjkajoča nalepka")
  ax[1][0].axis('off')
  ax[1][0].set_title("Brez parkirnega listka")
  ax[1][1].axis('off')
  ax[1][1].set_title("Prepovedano parkiranje")
  ax[1][2].axis('off')
  ax[1][2].set_title("Prepovedano parkiranje - čiščenje")
  ax[2][0].axis('off')
  ax[2][1].axis('off')
  ax[2][2].axis('off')

  plt.show()

draw_multiple_maps(csv_2017)

