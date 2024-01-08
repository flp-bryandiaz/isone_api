"""Module of classes that use the ISONE client to reach endpoints"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List


from isone_web_api.api_client import ISONEClient


def validate_date_format(date_text):
    """
    Validate that a date string is in the 'YYYYMMDD' format.

    This function checks if the provided date string adheres to the exact format
    of 4-digit year, 2-digit month, and 2-digit day ('YYYYMMDD'). If the format
    does not match, it raises a ValueError.

    Args:
        date_text (str): The date string to validate.

    Raises:
        ValueError: If the date string is not in the correct 'YYYYMMDD' format.
    """
    # Attempt to parse the date string into a datetime object with the expected format
    try:
        parsed_date = datetime.strptime(date_text, "%Y%m%d")
    except ValueError as wrong_format_error:
        # If parsing fails, the format is incorrect, and we raise a ValueError
        raise ValueError(
            f"The date {date_text} is not in the correct format YYYYMMDD."
        ) from wrong_format_error

    # If the parsing succeeds but the formatted string doesn't match the input,
    # it means the input was in a correct but not the expected format.
    if parsed_date.strftime("%Y%m%d") != date_text:
        raise ValueError(f"The date {date_text} is not in the strict format YYYYMMDD.")

    # If the input passes both checks, the function completes successfully,
    # indicating the date_text is in the correct format.


class DataRetriever(ABC):
    """
    Abstract base class for data retrieval.

    This class is designed to be subclassed by specific data retrievers that know
    how to interact with different endpoints of the API and retrieve data accordingly.

    Attributes:
        api_client (ISONEClient): A client instance to communicate with the API.
        record_path (list): A list that defines the path to the relevant section in the JSON data
                            structure returned from the API.
    """

    def __init__(self, api_client: ISONEClient, record_path: List[str]):
        """
        Initialize the data retriever with an API client and a record path.

        Args:
            api_client (ISONEClient): The API client to be used for making requests.
            record_path (List[str]): The path to navigate through the JSON data structure
                                     to find the relevant data.
        """
        self.api_client = api_client  # Stores the API client for HTTP communication
        self.record_path = (
            record_path  # Defines the path to data in the API's JSON response
        )

    @abstractmethod
    def retrieve_data(self, *args, **kwargs) -> Any:
        """
        Abstract method to retrieve data from the API.

        Subclasses must override this method to perform the actual data retrieval
        from the API based on the specific endpoint and parameters required.

        The method's parameters and return type can be specified by the concrete subclass
        to match the requirements of the specific API endpoint it interacts with.

        Returns:
            The data retrieved from the API, the type of which will depend on the
            implementation in the subclass (e.g., dict, list, DataFrame).
        """
        ...  # Implementation should be provided in subclasses


class DailyFuelMixDataRetriever(DataRetriever):
    """
    A concrete data retriever for obtaining daily fuel mix data from the API.

    This class extends DataRetriever, providing a specific implementation for retrieving
    the daily fuel mix data from the ISO New England's API.

    Inherits all attributes from DataRetriever:
        api_client (ISONEClient): A client instance to communicate with the API.
        record_path (list): A list defining the path to the daily fuel mix section in
                            the API's JSON response structure.
    """

    def __init__(self, api_client: ISONEClient):
        """
        Initialize the daily fuel mix data retriever with the API client.

        Args:
            api_client (ISONEClient): The API client to be used for making requests.

        The record path is set to navigate the JSON response structure to reach the
        daily fuel mix data.
        """
        # Record path points to the specific data in the API response for daily fuel mixes.
        super().__init__(api_client, record_path=["GenFuelMixes", "GenFuelMix"])

    def retrieve_data(self, day: str):
        """
        Retrieve the daily fuel mix data for a given day.

        Args:
            day (str): A string representing the day in the format 'YYYYMMDD' for which
                       the data is to be retrieved.

        Returns:
            A dictionary or a string formatted JSON response containing the daily fuel mix data.

        Raises:
            ValueError: If the 'day' is not in the correct format.
        """
        # Validates the date format before making the API call
        validate_date_format(day)
        # Constructs the endpoint using the provided day
        endpoint = f"genfuelmix/day/{day}"
        # Uses the API client to get the data from the constructed endpoint
        return self.api_client.get_data(endpoint=endpoint)
