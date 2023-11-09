from flask import Flask, render_template, request
from application import func

app = Flask(__name__)


@app.route("/")
def index():
    message = "Välkommen till min individuella uppgift!"
    return render_template("index.html", message=message)


@app.route("/form")
def form():
    # Hanterar anrop till "form"-endpointen.
    max_date = func.get_max_date()
    return render_template("form.html", max_date=max_date)


@app.route("/api", methods=["POST"])
def api_post():
    try:
        date = request.form["date"]
        year, month, day = date.split('-')
        priceclass = request.form["prisklass"]
        api_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{priceclass}.json"

        table = func.pandas_df_to_html_table(api_url)

        return render_template("table.html", table=table, date=date, priceclass=priceclass)
    except ValueError as ve:
        '''Felhantering för tomt datum fält i "/form" endpoint.
        Laddar "/api" endpoint men skickar istället med "form.html"
        templaten och ett felmeddelande.'''
        max_date = func.get_max_date()
        return render_template("form.html", max_date=max_date, error=ve)


@app.route("/api", methods=["GET"])
def api_get():
    # Aktiveras om man försöker komma åt "/api"-endpointen med "GET"-metoden.
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    message = "Ogiltigt val!"
    return render_template("index.html", message=message), 404


