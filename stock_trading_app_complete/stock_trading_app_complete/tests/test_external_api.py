import pytest
import requests
from external_api import fetch_stock_price, lookup

def test_fetch_stock_price_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"Global Quote": {"05. price": "123.45"}}
    mocker.patch("requests.get", return_value=mock_response)
    price = fetch_stock_price("AAPL")
    assert price == 123.45

def test_fetch_stock_price_failure(mocker):
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Fail"))
    with pytest.raises(RuntimeError, match="External API request failed"):
        fetch_stock_price("AAPL")

def test_lookup_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "bestMatches": [{"1. symbol": "AAPL", "2. name": "Apple Inc"}]
    }
    mocker.patch("external_api.requests.get", return_value=mock_response)

    result = lookup("AAPL")
    assert result["1. symbol"] == "AAPL"

def test_lookup_no_match(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"bestMatches": []}
    mocker.patch("external_api.requests.get", return_value=mock_response)

    result = lookup("XXXX")
    assert result == {}

