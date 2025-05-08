"""
Flask application factory and route definitions.

this module configures and creates the Flask app, initializes database and login
managers, and registers blueprints for authentication, stock, and portfolio routes.

it also defines core application-level routes (e.g., healthcheck), custom error handlers,
and helper functions for session validation and request payload validation.

environment variables are loaded using python-dotenv.

globals:
    db (SQLAlchemy): database instance used across the app.
    login_manager (LoginManager): Flask-Login manager instance.
"""

from flask import Flask
from flask import request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import logging
import external_api


# configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Ensure fetch_stock_price and portfolio are imported or instantiated
from external_api import fetch_stock_price
from models.portfolio_model import portfolio_model as portfolio

def validate_json(keys):
    """
    validate presence of required keys in the JSON request body.

    args:
        keys (list): a list of expected keys.

    returns:
        dict: the validated JSON data.

    raises:
        ValueError: if any required key is missing.
    """
    data = request.get_json() or {}
    for k in keys:
        if k not in data:
            raise ValueError(f"Missing required field '{k}'")
    return data

def require_login():
    """
    verify that a user is logged in via session data.

    raises:
        ValueError: if 'user_id' is not in session.
    """
    if 'user_id' not in session:
        raise ValueError('Unauthorized')


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """
    application factory for creating and configuring the Flask app instance.

    this function initializes the Flask app, sets up configuration using
    environment variables, initializes the SQLAlchemy and Flask-Login extensions,
    registers blueprints for modular routing, and defines application-level routes
    and error handlers.

    returns:
        Flask: the fully configured Flask application instance.
    """
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
        """
        health check endpoint to verify that the application is running.

        returns:
            response: JSON response indicating application status (200 OK).
        """
        logger.info("Healthcheck OK")
        return jsonify({"status": "ok"}), 200

    @app.route('/portfolio/buy', methods=['POST'])
    def buy_stock():
        """
        buy a stock for the currently logged-in user.

        expects a JSON payload with:
            - symbol (str): stock ticker symbol (e.g., "AAPL").
            - quantity (int): number of shares to purchase.

        looks up the current stock price, adds the holding to the user's portfolio,
        and returns a confirmation message with transaction details.

        returns:
            response: JSON response with purchase summary (200 OK).
        """
        require_login()
        logger.info(f"User {session.get('user_id')} attempting to BUY")
        data = validate_json(['symbol', 'quantity'])
        symbol = data['symbol'].upper()
        qty = int(data['quantity'])
        price = fetch_stock_price(symbol)
        from models.user_model import Users
        user = Users.query.get(session['user_id'])
        portfolio.buy(user.username, symbol, qty, price)

        logger.info(f"Bought {qty} of {symbol} at {price}")
        return jsonify({
            'message': 'Stock purchased',
            'symbol': symbol,
            'quantity': qty,
            'price': price
        }), 200

    @app.route('/portfolio/holding/<symbol>', methods=['GET'])
    def get_holding(symbol):
        """
        retrieve information about a specific stock holding.

        args:
            symbol (str): the stock ticker symbol to retrieve.

        returns:
            response:
                - 200 OK with holding details if it exists.
                - 404 Not Found if the holding is not present.
        """
        require_login()
        h = portfolio.view(session['user_id']).get(symbol.upper())
        if not h:
            return jsonify({'error': 'No such holding'}), 404
        return jsonify({'symbol': symbol.upper(), **h}), 200

    @app.route('/portfolio/holding/<symbol>', methods=['DELETE'])
    def delete_holding(symbol):
        """
        delete a specific stock holding from the user's portfolio.

        args:
            symbol (str): the stock ticker symbol to remove.

        returns:
            response:
                - 200 OK if the holding is deleted.
                - 404 Not Found if the holding does not exist.
        """
        require_login()
        holdings = portfolio.get_holdings(session['user_id'])
        if symbol.upper() not in holdings:
            return jsonify({'error': 'No such holding'}), 404
        del holdings[symbol.upper()]
        return jsonify({'message': 'Holding deleted'}), 200

    @app.route('/portfolio/clear', methods=['DELETE'])
    def clear_portfolio():
        """
        remove all stock holdings from the user's portfolio.

        returns:
            response: JSON message confirming the portfolio was cleared (200 OK).
        """
        require_login()
        portfolio._data.pop(session['user_id'], None)
        logger.info(f"User {session['user_id']} cleared their portfolio")
        return jsonify({'message': 'Portfolio cleared'}), 200

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        """
        global error handler for ValueErrors.

        returns:
            response: 400 Bad Request with a JSON error message.
        """
        logger.warning(f"ValueError: {e}")
        return jsonify({'error': str(e)}), 400
    
    @app.errorhandler(404)
    def handle_404(e):
        """
        global handler for 404 Not Found errors.

        returns:
            response: 404 status code with a JSON error message.
        """
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        """
        global handler for unhandled server errors.

        returns:
            response: 500 Internal Server Error with a JSON error message.
        """
        logger.error(f"Server Error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


    return app