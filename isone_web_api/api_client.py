"""Module for functions to access ISO-NE API endpoints"""
import logging
import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


def load_environment_secrets(dotenv_path=None):
    """
    Loads API credentials from environment variables.

    Args:
    dotenv_path (str): Optional path to a dotenv file to load. If not provided, defaults to '.env'.

    Returns:
    tuple: A tuple containing the API username and password.

    Raises:
    RuntimeError: If the required environment variables are not set.
    """

    # Loading through dotenv is required to use the getenv method
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        load_dotenv()

    api_username = os.getenv("API_USERNAME")
    api_password = os.getenv("API_PASSWORD")

    if not api_username or not api_password:
        logging.error("API credentials not found in environment variables.")
        raise RuntimeError("API credentials are required but not set.")

    return api_username, api_password


class ISONEClient:
    """
    A client for interacting with the ISO New England API.

    This client handles the communication with the ISO New England's RESTful API,
    managing authentication and requests to the provided endpoints.

    Attributes:
        BASE_URL (str): Base URL for the ISO New England API.
        auth (HTTPBasicAuth): Authentication credentials for the API.

    Methods:
        get_data(endpoint, params=None, format="json"): Retrieve data from a specific endpoint.
    """

    BASE_URL = "https://webservices.iso-ne.com/api/v1.1"

    def __init__(self):
        """
        Initialize the API client with the necessary authentication credentials.
        """
        # Setup the HTTP Basic Authentication with the provided username and password
        username, password = load_environment_secrets()
        self.auth = HTTPBasicAuth(username, password)

    def get_data(self, endpoint, params=None, file_format="json"):
        """
        Send a GET request to a specific API endpoint and return the data.

        Args:
            endpoint (str): The specific API endpoint to target.
            params (dict, optional): The query parameters to include in the request.
            file_format (str, optional): The desired response format ('json' or 'xml').
                                         Defaults to 'json'.

        Returns:
            dict or str: Parsed JSON response if format is 'json', raw text if format is 'xml'.

        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        # Set the headers to request the specific data format
        headers = {"Accept": f"application/{file_format}"}
        # Construct the full URL including the endpoint and format extension
        url = f"{self.BASE_URL}/{endpoint}.{file_format}"

        # Perform the GET request with authentication and headers
        response = requests.get(url, auth=self.auth, headers=headers, params=params)

        # Raise an exception if the request was not successful
        response.raise_for_status()

        # Return the parsed JSON data or raw text, based on the requested format
        return response.json() if file_format == "json" else response.text
