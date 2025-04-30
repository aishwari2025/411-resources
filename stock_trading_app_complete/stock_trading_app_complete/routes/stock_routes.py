from flask import Blueprint, request, jsonify
from flask_login import login_required
import external_api  # import the module, not the function

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/stock/lookup", methods=["GET"])
@login_required
def lookup():
    symbol = request.args.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "Missing symbol"}), 400
    try:
        data = external_api.lookup(symbol)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
