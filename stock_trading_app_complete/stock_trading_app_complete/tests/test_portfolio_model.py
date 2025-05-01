from models.portfolio_model import portfolio

def test_buy_stock():
    portfolio.clear("user1")
    portfolio.buy("user1", "AAPL", 10)
    assert portfolio.view("user1")["AAPL"] == 10

def test_sell_stock():
    portfolio.clear("user1")
    portfolio.buy("user1", "AAPL", 10)
    portfolio.sell("user1", "AAPL", 5)
    assert portfolio.view("user1")["AAPL"] == 5

def test_sell_all_shares_removes_stock():
    portfolio.clear("user1")
    portfolio.buy("user1", "AAPL", 10)
    portfolio.sell("user1", "AAPL", 10)
    assert "AAPL" not in portfolio.view("user1")

def test_clear_portfolio():
    portfolio.buy("user1", "AAPL", 10)
    portfolio.clear("user1")
    assert portfolio.view("user1") == {}
