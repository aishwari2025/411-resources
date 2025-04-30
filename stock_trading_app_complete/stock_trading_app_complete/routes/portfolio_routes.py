from flask import Blueprint, request
from flask_login import login_required, current_user
from models.portfolio_model import portfolio_model
from api.stock_api import get_stock_quote

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/portfolio", methods=["GET"])
@login_required
def view_portfolio():
    return portfolio_model.view(current_user.username)

@portfolio_bp.route("/portfolio/buy", methods=["POST"])
@login_required
def buy():
    data = request.get_json()
    symbol = data["symbol"].upper()
    shares = int(data["quantity"])
    portfolio_model.buy(current_user.username, symbol, shares)
    return {"message": f"Bought {shares} shares of {symbol}"}

@portfolio_bp.route("/portfolio/sell", methods=["POST"])
@login_required
def sell():
    data = request.get_json()
    symbol = data["symbol"].upper()
    shares = int(data["quantity"])
    portfolio_model.sell(current_user.username, symbol, shares)
    return {"message": f"Sold {shares} shares of {symbol}"}

@portfolio_bp.route("/portfolio/value", methods=["GET"])
@login_required
def value():
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
    portfolio_model.clear(current_user.username)
    return {"message": "Portfolio cleared"}
