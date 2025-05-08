from dotenv import load_dotenv
from functools import lru_cache
load_dotenv()

import os
import requests

API_KEY   = os.getenv('ALPHA_VANTAGE_API_KEY')
if not API_KEY:
    raise RuntimeError("Missing ALPHA_VANTAGE_API_KEY in environment")
BASE_URL  = 'https://www.alphavantage.co/query'

@lru_cache(maxsize=128)
def fetch_stock_price(symbol: str) -> float:
    """
    Fetches the latest price for `symbol` from Alpha Vantage.
    Requires:
      - ALPHA_VANTAGE_API_KEY in environment
      - `requests` installed
    """
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol':   symbol,
        'apikey':   API_KEY
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"External API request failed: {e}")
    data = resp.json().get('Global Quote', {})
    return float(data.get('05. price', 0.0))

@lru_cache(maxsize=128)
def lookup(symbol: str) -> dict:
    """
    Looks up detailed stock information for a given symbol using Alpha Vantage.
    Returns a dictionary of key financial data, or an empty dict if not found.
    """
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': symbol,
        'apikey': API_KEY
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if "bestMatches" in data and len(data["bestMatches"]) > 0:
            return data["bestMatches"][0]
        return {}
    except requests.RequestException as e:
        raise RuntimeError(f"Lookup request failed: {e}")