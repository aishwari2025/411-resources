from flask import Blueprint, request
from flask_login import login_required
from api.stock_api import get_stock_quote

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/stock/lookup", methods=["GET"])
@login_required
def lookup():
    symbol = request.args.get("symbol").upper()
    data = get_stock_quote(symbol)
    return data
