"""
in-memory portfolio model for managing user stock holdings.

this module defines a simple class to track stock purchases, sales, and portfolio
value on a per-user basis. it is used in place of a persistent database and
is suitable for prototype or test environments.
"""

class portfolio:
    """
    a lightweight in-memory portfolio manager for user stock holdings.

    attributes:
        holdings (dict): a nested dictionary storing stock quantities by username.

    Example structure:
        {
            "alice": {"AAPL": 10, "TSLA": 5},
            "bob": {"GOOG": 2}
        }
    """
    def __init__(self):
        """
        initialize the portfolio with an empty holdings dictionary.
        """
        self.holdings = {}

    def buy(self, username, symbol, shares):
        """
        add shares of a stock to a user's portfolio.

        args:
            username (str): the user’s identifier.
            symbol (str): the stock ticker symbol (e.g., "AAPL").
            shares (int): number of shares to purchase.

        side effects:
            - updates or creates an entry in the user's portfolio.
        """
        self.holdings.setdefault(username, {})
        self.holdings[username][symbol] = self.holdings[username].get(symbol, 0) + shares

    def sell(self, username, symbol, shares):
        """
        remove shares of a stock from a user's portfolio.

        args:
            username (str): the user’s identifier.
            symbol (str): the stock ticker symbol.
            shares (int): number of shares to sell.

        side effects:
            - reduces the share count for the given stock.
            - removes the stock from the portfolio if count drops to zero.
        """
        if symbol in self.holdings.get(username, {}) and self.holdings[username][symbol] >= shares:
            self.holdings[username][symbol] -= shares
            if self.holdings[username][symbol] == 0:
                del self.holdings[username][symbol]

    def view(self, username):
        """
        view all stock holdings for a given user.

        args:
            username (str): the user’s identifier.

        returns:
            dict: a dictionary of stock symbols and share quantities.
        """
        return self.holdings.get(username, {})

    def clear(self, username):
        """
        remove all holdings for the given user.

        args:
            username (str): the user’s identifier.

        side effects:
            - resets the user's portfolio to an empty dictionary.
        """
        self.holdings[username] = {}

portfolio_model = portfolio()
