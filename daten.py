# Import von dem Flask Modul Flash
from flask import flash
# Import json Modul für Datenspeicherung
import json
# Import für ID generierung (Quelle: https://www.geeksforgeeks.org/generating-random-ids-using-uuid-python/)
import uuid

# Funktion um die Dateien zu laden
def daten_laden(jsondatei):
    datei = jsondatei

    # Versuchen die Datei zu finden und öffnen und den Dateiinhalt zu laden
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    # Wenn die Datei nicht gefunden wird ein leeres Dict zurückgeben
    except FileNotFoundError:
        datei_inhalt = {}
    return datei_inhalt

# Funktion um einen neuen Umsatz zu speichern
def umsatzspeichern(datei, lieferant, kunde, umsatz, jahr):
    # Versuchen die Datei zu finden und öffnen und den Dateiinhalt zu laden
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    # Wenn die Datei nicht gefunden wird ein leeres Dict zurückgeben
    except FileNotFoundError:
        datei_inhalt = {}

    # ID für den Umsatz generieren (Quelle: https://www.geeksforgeeks.org/generating-random-ids-using-uuid-python/)
    id = uuid.uuid1()

    # Einen neuen Umsatz als Eintrag in die Umsatz Datei speichern
    datei_inhalt[str(id)] = {'lieferant' : lieferant, 'kunde' : kunde, 'umsatz' : umsatz, 'jahr' : jahr}

    # Die Umsatz Datei neu Laden das sie direkt aktualisiert wird
    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file)

# Funktion für das Hinzufügen eines neuen Kunden oder Lieferanten
def saveNewEntryToFile(datei, list, name):
    # Versuchen die Datei zu finden und öffnen und den Dateiinhalt zu laden
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    # Wenn die Datei nicht gefunden wird ein leeres Dict zurückgeben
    except FileNotFoundError:
        datei_inhalt = {}

    # Der Liste einen neuen Eintrag hinzufügen
    datei_inhalt[list].append(name)

    # Die Datei neu Laden das sie direkt aktualisiert wird
    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file)

# Funktion um eine Umsatz zu löschen
def umsatzloeschen(id):
    # Versuchen die Umsatz Datei zu finden und öffnen und den Dateiinhalt zu laden
    try:
        with open('umsatz.json') as data_file:
            data = json.load(data_file)
    # Wenn die Datei nicht gefunden wird ein leeres Dict zurückgeben
    except FileNotFoundError:
        data = {}

    # ID löschen oder Nachricht ausgeben
    if id in data:
        # Wenn die ID vorhanden ist dann den Eintrag löschen
        del data[id]
    # Wenn sie nicht existiert dann Flash Nachricht zeigen
    else:
        # Flash Nachricht (Quelle: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/)
        flash('Diese ID ist nicht vorhanden', 'id')

    # Die Datei neu Laden das sie direkt aktualisiert wird
    with open('umsatz.json', 'w') as data_file:
        data = json.dump(data, data_file)