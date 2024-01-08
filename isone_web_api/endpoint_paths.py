"""Containers for endpoints and payload JSON paths for ISO-NE API"""
from dataclasses import dataclass
from typing import List


@dataclass
class APIEndpoint:
    """Container for ISO-NE endpoints and JSON path"""

    endpoint_url: str  # Endpoint to ISO-NE API
    json_payload_record_path: List[str]  # List of string to locate JSON data


def create_endpoint_url(endpoint: APIEndpoint, parameters=dict):
    return endpoint.endpoint_url.format(parameters)


DailyFuelMix = APIEndpoint(
    endpoint_url="genfuelmix/day/{day}",
    json_payload_record_path=["GenFuelMixes", "GenFuelMix"],
)

