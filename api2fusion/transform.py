#Temporary Substitution for Some of Those City Names That Are Wrong By CAM2API Database
#Author: Anirudh Vegesana

import re

with open("cam_data.csv", encoding='utf-8') as f:
 content = f.readlines()

loc = {
 "Devil?sglen": "Devil's Glen",
 "Bed?ichov": "Bedřichov",
 "Pecpodsne?kou": "Pec pod Sněžkou",
 "?agarkalns": "Žagarkalns",
 "Bia?katatrza?ska": "Białka Tatrzańska",
 "????????(slavsko)": "Славське (Slavsko)",
 "????????(bukovel)": "Букавель (Bukovel)",
 "?????????(pamporovo)": "Пампорово (Pamporovo)",
 "????????(chepelare)": "Чепеларе (Chepelare)",
 "???????(borovets)": "Боровец (Borovets)",
 "?????????(kalavrita)": "Καλάβρυτα (Kalavryta)",
 "?????????????(krasnayapolyana)": "Красная Поляна (Krasnaya Polyana)",
 "Lesmontsd?olmes": "Les Monts d'Olmes",
 "?enkovice": "Čenkovice",
 "Novém?stonamorav?": "Nové Město na Moravě",
 "Pet?íkov": "Petříkov",
 "P?emyslov": "Přemyslov",
 "Bjela?nica": "Bjelašnica",
 "?trbsképleso": "Štrbské Pleso",
 "????(séli)": "Κάτω Βέρμιο Σέλι (Séli)",
 "Vy?náboca": "Vyšná Boca",
 "De?tné": "Deštné",
 "Kola?in": "Kolašin",
 "?pi?ák": "Špičák",
 "Je?t?d": "Ještěd",
 "Ve?kára?a": "Veľká Rača",
 "Ciudad Acu\\\\%ufffda": "Ciudad Acuña",
 "Le Val Sain-p\\%ufffdre": "Le Val-Saint-Père",
 "H%ufffdrtgenwald-vossenack": "Hürtgenwald-Vossenack",
 "H%ufffdrtgenwald-vossenack": "Hürtgenwald-Vossenack",
 "%u0410%u043d%u0430%u043f%u0430": "Anapa (Анапа)",
 "Vall%ufffda": "Vallåkra",
 "C%ufffdsa%u0159ov": "Císařov",
 "http%3A//": "http://",
 "Pol?ana": "Poľana",
 "?aclé?-prkennýd?l": "Žacléř-Prkenný Důl",
}

loc = {re.escape(k): v for k, v in loc.items()}
pattern = re.compile("|".join(loc.keys()))

with open("cam_data.csv", "w", encoding="utf8") as f:
 for text in content:
  f.write(pattern.sub(lambda m: loc[re.escape(m.group(0))], text))
 f.close()
print("Finish transform!")
