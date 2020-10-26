from flask import Flask
from flask import render_template
import daten

app = Flask("iSales")


@app.route('/hello')
def hello_world():
    return render_template('index.html', name="Fabian")

@app.route('/umsatz')
def get_revenue():
    revenues = daten.aktivitaeten_laden()

    return render_template('index.html', revenues=revenues)

@app.route("/speichern/<aktivitaet>")
def speichern(aktivitaet):
    zeitpunkt, aktivitaet = daten.aktivitaet_speichern(aktivitaet)

    return "Gespeichert: " + "etwas" + " um " + str("jetzt")

@app.route("/liste")
def auflisten():
    aktivitaeten = daten.aktivitaeten_laden()

    aktivitaeten_liste = ""
    for key, value in aktivitaeten.items():
        zeile = str(key) + ": " + value + "<br>"
        aktivitaeten_liste += zeile

    return aktivitaeten_liste




if __name__ == "__main__":
    app.run(debug=True, port=5000)
