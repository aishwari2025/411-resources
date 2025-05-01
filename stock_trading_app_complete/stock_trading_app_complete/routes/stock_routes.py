"""
routes for handling stock-related operations.

this module defines API endpoints for retrieving stock data via external API
calls. all routes require user authentication.
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required
import external_api  # import the module, not the function

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/stock/lookup", methods=["GET"])
@login_required
def lookup():
    """
    retrieve real-time stock quote data for a given symbol.

    this route expects a 'symbol' query parameter and returns JSON-formatted
    quote data retrieved via the external Alpha Vantage API. authentication is
    required.

    query Parameters:
        symbol (str): the stock ticker symbol to look up (e.g., "AAPL").

    returns:
        - 200 OK with quote data if successful.
        - 400 Bad Request if the symbol is missing.
        - 500 Internal Server Error if an exception occurs during the API call.
    """
    symbol = request.args.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "Missing symbol"}), 400
    try:
        data = external_api.lookup(symbol)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
