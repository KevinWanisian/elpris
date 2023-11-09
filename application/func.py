import ssl
import json
from urllib import request
from urllib import error
import pandas as pd
from datetime import datetime, timedelta


def json_data_to_pandas_df(api_url):
    '''Konverterar JSON-data till en pandas DataFrame.'''
    context = ssl._create_unverified_context()
    json_data = request.urlopen(api_url, context=context).read()  # Läs JSON-data från den angivna URL:en
    data = json.loads(json_data)  # Konvertera JSON-data till ett Python-dictionary
    df = pd.DataFrame(data)  # Skapa en pandas DataFrame från det konverterade datat
    return df


def pandas_df_to_html_table(api_url, columns=None):
    '''Konverterar en pandas DataFrame till en HTML-tabell'''
    try:
        df = json_data_to_pandas_df(api_url)  # Hämta data som en pandas DataFrame

        # Ändra namnen på kolumnerna
        df.columns = ["SEK per KWH", "EUR per KWH", "Tid"]

        df['Tid'] = pd.to_datetime(df['Tid'])

        # Ändrar datum till ett önskat format
        df['Tid'] = df['Tid'].dt.strftime('%H:%M')

        # Ta bort vissa kolumner (EXR och Time_end) från DataFrame
        df.drop(df.columns[2], axis=1, inplace=True)
        df.drop(df.columns[3], axis=1, inplace=True)

        # Skapa en HTML-tabell från DataFrame med specifika klasser och justering
        if columns is None:
            table_data = df.to_html(classes="table p-5", justify="left")
        else:
            table_data = df.to_html(columns=columns, classes="table p-5", justify="left")

        return table_data  # Returnera den skapade HTML-tabellen
    except Exception as e:
        # Hantera eventuella fel som kan uppstå under bearbetningen av data
        if isinstance(e, error.HTTPError) and e.code == 404:
            return "Morgondagens elpriser har inte publicerats ännu."

        return "Ett fel uppstod. Kontakta administratören för hjälp."


def get_max_date():
    '''Returnerar en sträng med morgondagens datum i formatet "yyyy-mm-dd".'''
    date = datetime.today()
    new_date = date + timedelta(days=1)
    day = new_date.day
    month = new_date.month
    year = new_date.year
    max_date = f"{year}-{month:02d}-{day:02d}"  # Formatera datumsträngen med ledande noll för månader och dagar

    return max_date
