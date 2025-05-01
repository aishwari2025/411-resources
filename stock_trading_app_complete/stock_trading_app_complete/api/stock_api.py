"""
module for interacting with the Alpha Vantage stock API.

this module provides a helper function to fetch real-time stock quote data
from the Alpha Vantage API using the 'GLOBAL_QUOTE' function.

requires:
    - a valid API key set in the ALPHA_VANTAGE_KEY variable (imported from config).
"""

import requests
import os
from config import ALPHA_VANTAGE_KEY

BASE_URL = "https://www.alphavantage.co/query"

def get_stock_quote(symbol):
    """
    fetch the latest stock quote for a given symbol from Alpha Vantage.

    args:
        symbol (str): the stock ticker symbol (e.g., "AAPL", "MSFT").

    returns:
        dict: a dictionary containing stock quote data under the "Global Quote" key.
              returns an empty dictionary if the quote is unavailable or malformed.
    """
    response = requests.get(BASE_URL, params={
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_KEY
    })
    data = response.json()
    return data.get("Global Quote", {})
