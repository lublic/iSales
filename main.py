# Import von den Flask Modulen
from flask import Flask
from flask import flash
from flask import render_template
from flask import request
# Import von Plotly für die Datenvisualisierung (Quelle: https://plotly.com/python/bar-charts/)
import plotly.express as px
import plotly
# Import der Pythondatei daten
import daten
# Import der Pythondatei filter
import filter

# Initialisieren von Flask und App Benennung "iSales"
app = Flask("iSales")
# Schlüssel für die Verschlüsselung der Flash Nachricht (Quelle: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# App Route für die Home Seite
@app.route('/')
def home():
    return render_template('index.html')

# App Route für die Seite der Datenausgabe
@app.route('/output', methods=['GET', 'POST'])
def get_revenue():
    # Umsatz laden
    revenues = daten.daten_laden("umsatz.json")

    # liste mit den gefilterten Umsätzen erstellen
    revenues_filtered = revenues

    # "Alle" als Dropdown beim Filter auswählen
    selected_jahr = selected_kunde = selected_lieferant = "Alle"

    # Wenn gefiltert wird dann...
    if request.method == 'POST':
        # lösche alle Umsätze, welche nicht gewünscht sind
        revenues_filtered = filter.filter(revenues_filtered, 'jahr', request.form['jahr'])
        revenues_filtered = filter.filter(revenues_filtered, 'lieferant', request.form['lieferant'])
        revenues_filtered = filter.filter(revenues_filtered, 'kunde', request.form['kunde'])

        # Filter richtiges Dropdown item auswählen
        selected_jahr = request.form['jahr']
        selected_kunde = request.form['kunde']
        selected_lieferant = request.form['lieferant']

    # Listen für die Dropdown filter erstellen
    filter_list_jahr = filter.getFilterList(revenues, 'jahr', selected_jahr)
    filter_list_lieferant = filter.getFilterList(revenues, 'lieferant', selected_lieferant)
    filter_list_kunde = filter.getFilterList(revenues, 'kunde', selected_kunde)

    # Liste für die gefilterten Umsätze
    sumlist = []

    # Die gefilterten Umsätze in die sumlist hinzufügen
    for k, v in revenues_filtered.items():
        # Füge Item der Liste hinzu
        sumlist.append(v['umsatz'])

    # Summe der gefilterten Umsätze erstellen
    summe_umsatz = sum(sumlist)

    # Liste für die gefilterten Jahre
    yearlist = []

    # Die gefilterten Jahre in die yearlist hinzufügen
    for k, v in revenues_filtered.items():
        # Füge Item der Liste hinzu
        yearlist.append(v['jahr'])

    # Datenvisualisierung der Umsätze (Quelle: https://plotly.com/python/bar-charts/)
    fig = px.bar(x=yearlist, y=sumlist)
    div = plotly.io.to_html(fig, include_plotlyjs=True, full_html=False)

    # Ausgabe für das Html Datenausgabe
    return render_template('datenausgabe.html', revenues=revenues_filtered, filter_list_jahr=filter_list_jahr, filter_list_lieferant=filter_list_lieferant, filter_list_kunde=filter_list_kunde, summe_umsatz = summe_umsatz, viz_div = div)

# App Route für die Seite der Dateneingabe
@app.route("/input", methods=['GET', 'POST'])
def auflisten():
    # Jahres Liste laden
    jahre = daten.daten_laden("jahre.json")

    # Lieferanten Liste laden
    lieferanten = daten.daten_laden("lieferanten.json")

    # Kunden Liste laden
    kunden = daten.daten_laden("kunden.json")

    # Daten aus den json Listen holen
    year_list = filter.eingabefilter(jahre, 'jahre')
    lif_list = filter.eingabefilter(lieferanten, 'lieferanten')
    kund_list = filter.eingabefilter(kunden, 'kunden')

    # Eingabe Formulare für neuen Umsatz, neuer Kunde oder Lieferant und Umsatz löschen
    if request.method == 'POST':
        # Eingabe für einen neuen Umsatz
        if request.form['submit'] == 'Umsatz eintragen':
            eingabe_umsatz = request.form['eingabe_umsatz']
            eingabe_jahr = request.form['year_list']
            eingabe_lieferant = request.form['lif_list']
            eingabe_kunde = request.form['kund_list']

            # Speichern des oben eingetragen Umsatz in die Umsatz.json
            daten.umsatzspeichern('umsatz.json', eingabe_lieferant, eingabe_kunde, int(eingabe_umsatz), eingabe_jahr)

        # Eingabe für einen neuen Kunde oder Lieferant
        if request.form['submit'] == 'Eintrag erstellen':
            eingabe_newkunde = request.form['eingabe_newkund']
            eingabe_newlieferant = request.form['eingabe_newlief']

            # Überprüfen ob es den Kunden schon gibt
            if eingabe_newkunde:
                # Wenn der Kunde existiert gibt es eine Meldung
                if any(eingabe_newkunde in s for s in kund_list):
                    # Flash Benachrichtigung Kunde (Quelle: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/)
                    flash('Dieser Kunde existiert bereits', 'kundeorlieferant')
                # Wenn der Kunde nicht existiert wird er in die Kundenliste abgespeichert
                else:
                    daten.saveNewEntryToFile('kunden.json', 'kunden', eingabe_newkunde)
                    kund_list.append(eingabe_newkunde)
                    kund_list.sort()

            # Überprüfen ob es den Lieferant schon gibt
            if eingabe_newlieferant:
                # Wenn der Lieferant existiert gibt es eine Meldung
                if any(eingabe_newlieferant in s for s in lif_list):
                    # Flash Benachrichtigung Lieferant (Quelle: https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/)
                    flash('Dieser Lieferant existiert bereits', 'kundeorlieferant')
                # Wenn der Lieferant nicht existiert wird er in die Lieferantenliste abgespeichert
                else:
                    daten.saveNewEntryToFile('lieferanten.json', 'lieferanten', eingabe_newlieferant)
                    lif_list.append(eingabe_newlieferant)
                    lif_list.sort()

        # Eingabe für Umsatz löschung
        if request.form['submit'] == 'Umsatz löschen':
            # Eingabe ID eines Umsatzes
            eingabe_id = request.form['eingabe_id']
            # Funktion um den Umsatz zu löschen
            daten.umsatzloeschen(eingabe_id)

    # Ausgabe für das Html Dateneingabe
    return render_template('dateneingabe.html', year_list=year_list, lif_list=lif_list, kund_list=kund_list)

# Parameter Debugging eingeschaltet und es soll auf dem Rechner Port 5000 laufen
if __name__ == "__main__":
    app.run(debug=True, port=5000)
