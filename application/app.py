from flask import Flask, render_template, request
from application import func

app = Flask(__name__)




@app.route("/")
def index():
    '''Hanterar anrop till roten av applikationen.'''
    message = "Välkommen till min individuella uppgift!"
    return render_template("index.html", message=message)  # Rendera "index.html"-templaten med ett välkomstmeddelande

@app.route("/form")
def form():
    '''Hanterar anrop till "form"-endpointen.'''
    max_date = func.get_max_date()  # Hämta max datum från applikationsmodulen
    return render_template("form.html", max_date=max_date)

@app.route("/api", methods=["POST"])
def api_post():
    try:
        date = request.form["date"]  # Hämta datum från formuläret i POST-requesten
        year, month, day = date.split('-')  # Dela upp datumet i år, månad och dag tydliget med "-"
        price = request.form["prisklass"]  # Hämta prisklassen från formuläret i POST-requesten
        api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price}.json"

        table = func.pandas_df_to_html_table(api_url)  # Skapa en HTML-tabell från API-responsen

        return render_template("table.html", table=table, date=date, price=price)
    except ValueError as ve:
        '''Felhantering för tomt datum fält i "/form" endpoint.'''
        max_date = func.get_max_date()
        return render_template("form.html", max_date=max_date, error=ve)

@app.route("/api", methods=["GET"])
def api_get():
    '''Aktiveras om man försöker komma åt "/api"-endpointen med "GET"-metoden.'''
    return render_template("index.html")  # Rendera "index.html"-templaten

@app.errorhandler(404)
def page_not_found(error):
    '''Hanterar 404-fel och renderar en anpassad felmeddelande-sida med en "tillbaka" knapp'''
    message = "ERROR 404!"
    return render_template("index.html", message=message), 404
