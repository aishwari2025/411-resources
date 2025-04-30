class portfolio:
    def __init__(self):
        self.holdings = {}

    def buy(self, username, symbol, shares):
        self.holdings.setdefault(username, {})
        self.holdings[username][symbol] = self.holdings[username].get(symbol, 0) + shares

    def sell(self, username, symbol, shares):
        if symbol in self.holdings.get(username, {}) and self.holdings[username][symbol] >= shares:
            self.holdings[username][symbol] -= shares
            if self.holdings[username][symbol] == 0:
                del self.holdings[username][symbol]

    def view(self, username):
        return self.holdings.get(username, {})

    def clear(self, username):
        self.holdings[username] = {}

portfolio_model = portfolio()
