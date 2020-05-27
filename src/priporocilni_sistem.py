from geopy.geocoders import Nominatim

# preberemo kordinate kazni in jih shranimo v spremenljivko "kordinati"
with open('../podatki/koordinate.txt', 'r') as file:
    koordinati = []
    for line in file:
        lati, long = line.split(",")
        lati = float(lati)
        long = float(long)
        if 40.4 < lati and lati < 41:
            if -74.3 < long and long < -73.7:
                koordinati.append((long, lati))

# inicializiramo 60x60 2d list, kjer bomo hranili število kazni na posameznem kvadratku:
case_grid = [[0 for col in range(60)] for row in range(60)]

# napolnimo kvadratke z številom kazni
for cord in koordinati:
    long_indx = round(float(cord[0] - (-74.3)) * 100) - 1
    lati_indx = round(float(cord[1] - 40.4) * 100) - 1
    case_grid[long_indx][lati_indx] += 1

# uporabnika povprašamo o trenutni lokaciji:
curr_addr = input("vnesite trenutni naslov v NYC: ")
geolocator = Nominatim(user_agent="test")
loc = geolocator.geocode(curr_addr + ',' + 'New York City, USA')
# če uporabnik vnese ne veljavno lokacijo:
if (loc is None):
    print('Ni podatkov o tej lokaciji')
# če uporabnik vnese veljavno lokacijo:
else:
    curr_addr_cord = [loc.longitude, loc.latitude]
    # izračunamo indekse kvadratka trenutne lokacije:
    curr_addr_long_indx = round(float(curr_addr_cord[0] - (-74.3)) * 100) - 1
    curr_addr_lati_indx = round(float(curr_addr_cord[1] - 40.4) * 100) - 1
    # nastavimo best score in best index na naslov kjer se trenutno nahajamo:
    best_score = case_grid[curr_addr_long_indx][curr_addr_lati_indx]
    best_indx = [curr_addr_long_indx, curr_addr_lati_indx]

    for i in range (curr_addr_long_indx - 1, curr_addr_long_indx + 1):
        for j in range (curr_addr_lati_indx - 1, curr_addr_lati_indx + 1):
            # da ne gledamo še 1x istega kordinate kjer se nahajamo trenutno:
            if i != curr_addr_long_indx or j != curr_addr_lati_indx:
                # če dobimo boljšo lokacijo shranimo boljši score in indeks najboljšega scora:
                if case_grid[i][j] * 1.2 < best_score:
                    best_score = case_grid[i][j]
                    best_indx = [i, j]


    # index nazaj v kordinate:
    best_long_cord = float((best_indx[0] + 1) / 100 - 74.3)
    best_lati_cord = float((best_indx[1] + 1) / 100 + 40.4)
    lat_long = f'{best_lati_cord}, {best_long_cord}'
    if curr_addr_long_indx == best_indx[0] and curr_addr_lati_indx == best_indx[1]:
        print('nahajate se na najboljši lokaciji za ilegalno parkiranje v svoji bližini')
    else:
        print('Najboljša lokacija za ilegalno parkiranje v tvoji bližini je:', geolocator.reverse(lat_long))
