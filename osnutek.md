# Parkirne kazni v NYC

## Opis podatkov
Podatke smo pridobili iz: https://www.kaggle.com/new-york-city/nyc-parking-tickets#Parking_Violations_Issued_-_Fiscal_Year_2017.csv

V podatkih imamo veliko podatkov o parkirnih kaznih v NYC od avgusta 2013 do konca leta 2017. Za vsak primer kazni imamo na voljo sledeče podatke:
- podatki o avtomobilu (npr. firma, tip, barva, registracija, ...)
- podatki o lokaciji (npr. okrožje, ulica, križišče, ...)
- podatki o enoti, ki je izdala kazen (npr. enota, oseba, ...)
- časovni podatki (npr. čas in datum kršitve, čas prve opazitve,...)
- podatki o kazni (npr. koda kazni, opis, ...)

kateri so skupaj shranjeni v do 53 atributov. Te podatke bomo po potrebi združevati s pomožnimi, kot so na primer prihodek glede na lokacijo 
v mestu v primeru, da bomo želeli opazovati povezavo med številom kazni v revnejših in bogatejših okrožjih.

## Opis problema
Iz podatkov bomo v glavnem razbirali katere karakteristike avtomobilov doprinesejo k večjem tveganju za parkirno kazen, ob katerih urah so mestni redarji najbolj aktivni,
v katerih obdobjih se napiše največ kazni (vikendi, prazniki, ...), katera agencija je bolj dejavna v določenih predelih mesta, ali celo kateri posameznik je izpisal največ kazni,
ali so redarji do katerih držav registracije pristranski oziroma ali katero okrožje izstopa po številu prejetih kazni in tako dalje.
