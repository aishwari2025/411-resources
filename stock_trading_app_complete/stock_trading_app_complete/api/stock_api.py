import requests
import os
from config import ALPHA_VANTAGE_KEY

BASE_URL = "https://www.alphavantage.co/query"

def get_stock_quote(symbol):
    response = requests.get(BASE_URL, params={
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_KEY
    })
    data = response.json()
    return data.get("Global Quote", {})
