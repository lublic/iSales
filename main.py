from flask import Flask
from flask import render_template
from flask import request
import daten
import filter

app = Flask("iSales")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/output', methods=['GET', 'POST'])
def get_revenue():
    # Umsatz laden
    revenues = daten.umsatz_laden()

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

    return render_template('datenausgabe.html', revenues=revenues_filtered, filter_list_jahr=filter_list_jahr, filter_list_lieferant=filter_list_lieferant, filter_list_kunde=filter_list_kunde)

@app.route("/input", methods=['GET', 'POST'])
def auflisten():


    # Jahres Liste laden
    jahre = daten.jahre_laden()

    # Lieferanten Liste laden
    lieferanten = daten.lieferanten_laden()

    # Kunden Liste laden
    kunden = daten.kunden_laden()

    year_list = filter.eingabefilter(jahre)
    lif_list = filter.eingabefilter(lieferanten)
    kund_list = filter.eingabefilter(kunden)

    if request.method == 'POST':
        eingabe_umsatz = request.form['eingabe_umsatz']
        eingabe_jahr = request.form['year_list']
        eingabe_lieferant = request.form['lif_list']
        eingabe_kunde = request.form['kund_list']

        daten.umsatzspeichern('umsatz.json', eingabe_lieferant, eingabe_kunde, int(eingabe_umsatz), eingabe_jahr)


    return render_template('dateneingabe.html', year_list=year_list, lif_list=lif_list, kund_list=kund_list)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
