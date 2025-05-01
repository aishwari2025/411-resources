"""
routes for portfolio management operations.

this module defines authenticated endpoints for viewing, modifying, and evaluating
a user's stock portfolio. all routes require login and use an in-memory data model
(`portfolio_model`) to store portfolio state per user.
"""

from flask import Blueprint, request
from flask_login import login_required, current_user
from models.portfolio_model import portfolio_model
from api.stock_api import get_stock_quote

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/portfolio", methods=["GET"])
@login_required
def view_portfolio():
    """
    retrieve the current user's stock portfolio.

    returns:
        dict: a dictionary of stock symbols and quantities.
    """
    return portfolio_model.view(current_user.username)

@portfolio_bp.route("/portfolio/buy", methods=["POST"])
@login_required
def buy():
    """
    buy a specified quantity of a stock and add it to the user's portfolio.

    request JSON:
        - symbol (str): the stock ticker symbol to buy.
        - quantity (int): the number of shares to purchase.

    returns:
        dict: a success message indicating the quantity and symbol purchased.
    """
    data = request.get_json()
    symbol = data["symbol"].upper()
    shares = int(data["quantity"])
    portfolio_model.buy(current_user.username, symbol, shares)
    return {"message": f"Bought {shares} shares of {symbol}"}

@portfolio_bp.route("/portfolio/sell", methods=["POST"])
@login_required
def sell():
    """
    sell a specified quantity of a stock from the user's portfolio.

    request JSON:
        - symbol (str): the stock ticker symbol to sell.
        - quantity (int): the number of shares to sell.

    returns:
        dict: a success message indicating the quantity and symbol sold.
    """
    data = request.get_json()
    symbol = data["symbol"].upper()
    shares = int(data["quantity"])
    portfolio_model.sell(current_user.username, symbol, shares)
    return {"message": f"Sold {shares} shares of {symbol}"}

@portfolio_bp.route("/portfolio/value", methods=["GET"])
@login_required
def value():
    """
    calculate the total value of the user's portfolio based on current stock prices.

    this route retrieves the user's holdings and fetches the current price for each stock
    using the external stock API. It returns the aggregated value in USD.

    returns:
        dict: the total portfolio value in the form {"portfolio_value": float}.
    """
    total = 0.0
    holdings = portfolio_model.view(current_user.username)
    for sym, qty in holdings.items():
        quote = get_stock_quote(sym)
        price = float(quote.get("05. price", 0))
        total += price * qty
    return {"portfolio_value": total}

@portfolio_bp.route("/portfolio/clear", methods=["DELETE"])
@login_required
def clear():
    """
    clear all holdings from the current user's portfolio.

    returns:
        dict: a message confirming the portfolio has been cleared.
    """
    portfolio_model.clear(current_user.username)
    return {"message": "Portfolio cleared"}
