"""An example implementation from starting the client to parsing a response to a DataFrame"""
from isone_web_api.api_client import ISONEClient
from isone_web_api.endpoints import DailyFuelMixDataRetriever
from isone_web_api.json_parser import parse_json_response

if __name__ == "__main__":
    # Initialize a client to connect to the ISO and act as a container for credentials
    client = ISONEClient()

    # Use the client to retrieve data from the endpoint
    endpoint = DailyFuelMixDataRetriever(client)
    endpoint_response = endpoint.retrieve_data("20231201")

    # Parse the JSON to a DataFrame
    # In our current implementation, the record_path is a property of the specific DataRetriever
    response_df = parse_json_response(endpoint_response, endpoint.record_path)
