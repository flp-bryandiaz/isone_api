"""Parsers for responses from ISO-NE API"""
import pandas as pd


def parse_json_response(data, record_path: list = None) -> pd.DataFrame:
    """
    Transforms nested JSON into a pandas DataFrame.

    :param data: dict, the JSON data returned from the API.
    :param record_path: list, the path (as a list of keys) to the nested data.
    :return: DataFrame containing the nested data.
    """
    if record_path:
        nested_data = data
        for key in record_path:
            nested_data = nested_data.get(key, [])
            if not nested_data:
                raise KeyError(f"Key '{key}' not found in the provided data.")
        if isinstance(nested_data, list):
            return pd.json_normalize(nested_data)
        else:
            raise TypeError("Nested data is not a list.")

    return pd.DataFrame(data)
