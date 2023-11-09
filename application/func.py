import ssl
import json
from urllib import request
from urllib import error
import pandas as pd
from datetime import datetime, timedelta


def json_data_to_pandas_df(api_url):
    '''Konverterar json data till en pandas dataframe'''
    context = ssl._create_unverified_context()
    json_data = request.urlopen(api_url, context=context).read()
    data = json.loads(json_data)
    df = pd.DataFrame(data)
    return df


def pandas_df_to_html_table(api_url, columns=None):
    '''Ändrar pandas dataframe html-tabell för min applikation'''
    try:
        df = json_data_to_pandas_df(api_url)
        # Tar bort EXR och time_end kolumnerna
        df.drop(df.columns[2], axis=1, inplace=True)
        df.drop(df.columns[3], axis=1, inplace=True)

        # Ändrar namnen på kolumnerna
        df.columns = ["SEK per KWH", "EUR per KWH", "Tid"]

        # Konvertera tidkolumnen till datetime-objekt
        df['Tid'] = pd.to_datetime(df['Tid'])

        # Formatera datumen som tidssträngar i ett önskat format
        df['Tid'] = df['Tid'].dt.strftime('%H:%M')

        if columns == None:
            table_data = df.to_html(classes="table p-5", justify="left")
        else:
            table_data = df.to_html(columns=columns, classes="table p-5", justify="left")

        return table_data
    except Exception as e:
        # Om man försöker ladda elpriser som inte har publicerats ännu.
        if isinstance(e, error.HTTPError) and e.code == 404:
            return "Morgondagens elpriser har inte publicerats ännu."

        # Plats för annan eventuell felhantering
        return "Ett fel uppstod. Kontakta administratören för hjälp."


def get_max_date():  # För att kunna ange vilket datum som är max i min form
    '''Returnerar en sträng med morgondagens datum
    i formatet "åååå-mm-dd'''
    date = datetime.today()
    new_date = date + timedelta(days=1)
    day = new_date.day
    month = new_date.month
    year = new_date.year
    max_date = f"{year}-{month:02d}-{day:02d}"

    return max_date
