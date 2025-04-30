from flask import Flask
from flask import request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import logging

# configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Ensure fetch_stock_price and portfolio are imported or instantiated
from external_api import fetch_stock_price
from models.portfolio_model import portfolio

def validate_json(keys):
    data = request.get_json() or {}
    for k in keys:
        if k not in data:
            raise ValueError(f"Missing required field '{k}'")
    return data

def require_login():
    """Ensure the user is logged in, or raise a ValueError."""
    if 'user_id' not in session:
        raise ValueError('Unauthorized')


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)
    login_manager.init_app(app)

    from models.user_model import Users
    from routes.auth_routes import auth_bp
    from routes.portfolio_routes import portfolio_bp
    from routes.stock_routes import stock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(stock_bp)

    @app.route('/healthcheck')
    def healthcheck():
        """Health check endpoint."""
        logger.info("Healthcheck OK")
        return jsonify({"status": "ok"}), 200

    @app.route('/portfolio/buy', methods=['POST'])
    def buy_stock():
        """Buy a stock for the logged-in user."""
        require_login()
        logger.info(f"User {session.get('user_id')} attempting to BUY")
        data = validate_json(['symbol', 'quantity'])
        symbol = data['symbol'].upper()
        qty = int(data['quantity'])
        price = fetch_stock_price(symbol)
        portfolio.buy(session.get('user_id'), symbol, qty, price)
        logger.info(f"Bought {qty} of {symbol} at {price}")
        return jsonify({
            'message': 'Stock purchased',
            'symbol': symbol,
            'quantity': qty,
            'price': price
        }), 200

    @app.route('/portfolio/holding/<symbol>', methods=['GET'])
    def get_holding(symbol):
        """Get details for a specific holding."""
        require_login()
        h = portfolio.view(session['user_id']).get(symbol.upper())
        if not h:
            return jsonify({'error': 'No such holding'}), 404
        return jsonify({'symbol': symbol.upper(), **h}), 200

    @app.route('/portfolio/holding/<symbol>', methods=['DELETE'])
    def delete_holding(symbol):
        """Delete a specific holding."""
        require_login()
        holdings = portfolio.get_holdings(session['user_id'])
        if symbol.upper() not in holdings:
            return jsonify({'error': 'No such holding'}), 404
        del holdings[symbol.upper()]
        return jsonify({'message': 'Holding deleted'}), 200

    @app.route('/portfolio/clear', methods=['DELETE'])
    def clear_portfolio():
        """Clear all holdings for the logged-in user."""
        require_login()
        portfolio._data.pop(session['user_id'], None)
        logger.info(f"User {session['user_id']} cleared their portfolio")
        return jsonify({'message': 'Portfolio cleared'}), 200

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        logger.warning(f"ValueError: {e}")
        return jsonify({'error': str(e)}), 400
    
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        logger.error(f"Server Error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


    return app