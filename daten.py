from datetime import datetime
import json


def speichern(datei, key, value):
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    datei_inhalt[str(key)] = value

    # print(datei_inhalt)

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file)


def aktivitaet_speichern(aktivitaet):
    datei_name = "umsatz.json"
    zeitpunkt = datetime.now()
    speichern(datei_name, zeitpunkt, aktivitaet)
    return zeitpunkt, aktivitaet


def umsatz_laden():
    umsatz = "umsatz.json"

    try:
        with open(umsatz) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt
