import json
import uuid


def umsatz_laden():
    umsatz = "umsatz.json"

    try:
        with open(umsatz) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

def lieferanten_laden():
    lieferanten = "lieferanten.json"

    try:
        with open(lieferanten) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

def kunden_laden():
    kunden = "kunden.json"

    try:
        with open(kunden) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

def jahre_laden():
    jahre = "jahre.json"

    try:
        with open(jahre) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt

def umsatzspeichern(datei, lieferant, kunde, umsatz, jahr):
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    id = uuid.uuid1()

    datei_inhalt[str(id)] = {'lieferant' : lieferant, 'kunde' : kunde, 'umsatz' : umsatz, 'jahr' : jahr}


    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file)