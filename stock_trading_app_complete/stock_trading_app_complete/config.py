"""
configuration module for environment variables.

this module loads environment variables from a `.env` file using `python-dotenv`
and exposes key constants for use throughout the application.

variables:
    SECRET_KEY (str): Flask secret key for session management.
    ALPHA_VANTAGE_KEY (str): API key for accessing the Alpha Vantage stock API.
"""

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
