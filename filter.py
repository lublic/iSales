# Liste mit DropDown Inhalt für Filter erstellen
def getFilterList(nestedDict, filter, selected_Filter):
    # Leere Liste erstellen
    filterList = []
    # Lade alle Items
    for k, v in nestedDict.items():
        # Füge Item der Liste hinzu
        filterList.append(v[filter])
    # Duplikate entfernen
    filterList = list(dict.fromkeys(filterList))
    # Liste sortieren
    filterList.sort()
    # "Alle" in Dropdown hinzufügen
    filterList.insert(0, "Alle")
    # Durch Filterliste gehen und das von User ausgwählte Dropdown selektieren
    i = 0
    for l in filterList:
        selected = ""
        if l == selected_Filter:
            selected = "selected=selected"
        filterList[i] = [l, selected]
        i += 1
    return filterList

# Funktion um die gefilterten Umsätze anzuzeigen
def filter(revenues_filtered, filter, selected_filter):
    if selected_filter != "Alle":
        revenues_filtered = {key: value for (key, value) in revenues_filtered.items() if
                             selected_filter in value[filter]}
    return revenues_filtered

# Funktion um die Jahre, Kunden und Lieferanten auszugeben
def eingabefilter(e_liste, inlist):
    # Liste für die Ausgabe
    eingabelist = []
    # Lade alle Items
    for v in e_liste.get(inlist):
        # Füge Item der Liste hinzu
        eingabelist.append(v)
    # Duplikate entfernen
    eingabelist = list(dict.fromkeys(eingabelist))
    # Liste sortieren
    eingabelist.sort()
    return eingabelist
