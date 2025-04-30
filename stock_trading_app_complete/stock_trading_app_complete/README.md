
# 📈 Stock Trading Web Application

## Overview
This Flask-based web application allows users to create an account, log in, manage a virtual stock portfolio (buy/sell stocks), and check real-time stock prices via Alpha Vantage API.

## Setup Instructions

1. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create your `.env` file**  
   (Use `.env.template` as a guide)
   ```
   SECRET_KEY=your_flask_secret_key
   ALPHA_VANTAGE_KEY=your_alpha_vantage_api_key
   ```

3. **Run the application**
   ```bash
   flask run
   ```

## Docker Instructions

1. **Build the Docker image**
   ```bash
   docker build -t stockapp .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 --env-file .env stockapp
   ```

## API Endpoints

### Health Check

- **Route:** `/healthcheck`
- **Method:** `GET`
- **Purpose:** Verify if the app is running
- **Response:** 
  ```json
  { "status": "ok" }
  ```

## Authentication Routes

### Create Account

- **Route:** `/create-account`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Example cURL:**
  ```bash
  curl -X POST http://localhost:5000/create-account -H "Content-Type: application/json" -d '{"username":"user1", "password":"pass123"}'
  ```

### Login

- **Route:** `/login`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Example cURL:**
  ```bash
  curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"user1", "password":"pass123"}'
  ```

### Logout

- **Route:** `/logout`
- **Method:** `POST`
- **Example cURL:**
  ```bash
  curl -X POST http://localhost:5000/logout
  ```

### Update Password

- **Route:** `/update-password`
- **Method:** `PUT`
- **Body:**
  ```json
  {
    "new_password": "your_new_password"
  }
  ```
- **Example cURL:**
  ```bash
  curl -X PUT http://localhost:5000/update-password -H "Content-Type: application/json" -d '{"new_password":"newpass456"}'
  ```

## Portfolio Management Routes

### View Portfolio

- **Route:** `/portfolio`
- **Method:** `GET`
- **Example cURL:**
  ```bash
  curl -X GET http://localhost:5000/portfolio
  ```

### Buy Stock

- **Route:** `/portfolio/buy`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "symbol": "AAPL",
    "quantity": 5
  }
  ```
- **Example cURL:**
  ```bash
  curl -X POST http://localhost:5000/portfolio/buy -H "Content-Type: application/json" -d '{"symbol":"AAPL", "quantity":5}'
  ```

### Sell Stock

- **Route:** `/portfolio/sell`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "symbol": "AAPL",
    "quantity": 2
  }
  ```
- **Example cURL:**
  ```bash
  curl -X POST http://localhost:5000/portfolio/sell -H "Content-Type: application/json" -d '{"symbol":"AAPL", "quantity":2}'
  ```

### View Portfolio Value

- **Route:** `/portfolio/value`
- **Method:** `GET`
- **Example cURL:**
  ```bash
  curl -X GET http://localhost:5000/portfolio/value
  ```


### Clear Portfolio

- **Route:** `/portfolio/clear`
- **Method:** `DELETE`
- **Example cURL:**
  ```bash
  curl -X DELETE http://localhost:5000/portfolio/clear
  ```

### Single Holding Endpoints

#### Get Single Holding
- **Route:** `/portfolio/holding/<symbol>`
- **Method:** `GET`
- **Purpose:** Retrieve details for a specific holding.
- **Example cURL:**
  ```bash
  curl -X GET http://localhost:5000/portfolio/holding/AAPL \
    -b cookies.txt
  ```
- **Successful Response:**
  ```json
  {
    "symbol": "AAPL",
    "quantity": 10,
    "avg_price": 135.50
  }
  ```
- **Errors:**
  - `401 Unauthorized` when not logged in:  
    ```json
    { "error": "Unauthorized" }
    ```
  - `404 Not Found` when the symbol is not held:  
    ```json
    { "error": "No such holding" }
    ```

#### Delete Holding
- **Route:** `/portfolio/holding/<symbol>`
- **Method:** `DELETE`
- **Purpose:** Remove a specific holding entirely.
- **Example cURL:**
  ```bash
  curl -X DELETE http://localhost:5000/portfolio/holding/AAPL \
    -b cookies.txt
  ```
- **Successful Response:**
  ```json
  { "message": "Holding deleted" }
  ```
- **Errors:**
  - `401 Unauthorized` when not logged in.
  - `404 Not Found` when the symbol is not held.

## Stock Lookup Route

### Lookup Stock Information

- **Route:** `/stock/lookup`
- **Method:** `GET`
- **Query Parameter:** `symbol`
- **Example cURL:**
  ```bash
  curl -X GET "http://localhost:5000/stock/lookup?symbol=MSFT"
  ```

## Testing Instructions

1. **Run all unit tests**
   ```bash
   pytest
   ```

# 🎯 Notes
- The application uses session-based login management with `Flask-Login`.
- Stocks are looked up in real-time from Alpha Vantage API.
- User authentication uses salted and hashed password storage.
- `.env` should never be committed to GitHub. Use `.env.template` instead.

- **Validation & Errors**  
  - Missing or invalid fields produce `400 Bad Request` with JSON:
    ```json
    { "error": "Missing required field 'symbol'" }
    ```
