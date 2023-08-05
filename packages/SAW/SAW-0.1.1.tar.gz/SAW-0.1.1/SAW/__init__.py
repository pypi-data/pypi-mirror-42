"""Wrapper module for the SimFin API

This module is the wrapper for the SimFin API. The module consists of three classes: HTTPClient,
Client and Company. The HTTPClient is the client used to make the HTTP requests to the API. Client
is the class used to manage the general connection and the class you should initialize to start
retreiving data. Company represents a company in the SimFin database and from this class you can
retrieve both fundamental and technical data.

Attributes:
	HTTP_CLIENT: The client used to make HTTP requests and apply rate limiting.
"""

from .http_client import HTTPClient
HTTP_CLIENT = HTTPClient()
from .client import Client
