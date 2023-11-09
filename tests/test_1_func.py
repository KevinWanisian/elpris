from application import func
import urllib.request
import ssl

context = ssl._create_unverified_context()


def test_is_online_index():
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)


def test_is_online_form():
    assert urllib.request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10)


def test_is_api():
    assert urllib.request.urlopen("http://127.0.0.1:5000/api", context=context, timeout=10)


def test_df():
    """Kontrollera om DataFrame har skapats"""
    api_url = "https://www.elprisetjustnu.se/api/v1/prices/2023/06-09_SE2.json"
    df = func.json_data_to_pandas_df(api_url)
    assert len(df) > 0


def test_pandas_html():
    """Skrev in värdet 2717 då det returnerades i binära tal istället för string."""
    api_url = "https://www.elprisetjustnu.se/api/v1/prices/2023/08-12_SE2.json"
    html_table = func.pandas_df_to_html_table(api_url)
    assert len(html_table) == 2717


def test_max_date():
    """Detta testar datumet"""
    max_date = func.get_max_date()
    assert len(max_date) == 10
