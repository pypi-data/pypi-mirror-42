import datetime
import requests

class HTTPClient():
    """HTTP client used to make HTTP request to the SimFin API and applying rate limiting."""
    def __init__(self):
        self.session = requests.Session()
        self.api_url = "https://simfin.com/api/v1"
        self.tokens = None
        self.last_refilled = None
        self.api_key = None
        self.simfin_plus = None

    def set_api_key(self, api_key, simfin_plus=False):
        """Set the API key

        Set the API key to be used to authenticate API request. Also specifies if account is a
        SimFin+ account, meaning no rate limit should be enforced.

        Args:
            api_key (str): The API key to use
            simfin_plus (bool): If account is SimFin+ or not (default: False)
        """
        self.tokens = 2000
        self.last_refilled = datetime.datetime.utcnow()
        self.api_key = api_key
        self.simfin_plus = simfin_plus

    def can_make_request(self):
        """Check rate limit allowance

        Checks if HTTPClient is allowed by the rate limiter to make request and handles refilling
        of token bucket.

        Returns:
            bool: True if allowed, false otherwise.
        """
        if self.simfin_plus:
            return True

        midnight = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if self.last_refilled < midnight:
            self.tokens = 2000
            self.last_refilled = datetime.datetime.utcnow()

        if self.tokens > 0:
            self.tokens -= 1
            return True

        return False


    def request(self, endpoint, query=None):
        """Make request to the API

        Generates a http request to the speciefied endpoint at the API with optional query data.

        Args:
            endpoint (str): Endpoint to access at the API
            query: Optional query data to send with the request (default: None)

        Returns:
            dict/list: response from the SimFin API
        """
        if not query:
            query = {}

        query_string = "".join(['&%s=%s' % (key, str(value)) for (key, value) in query.items()])
        url = self.api_url + endpoint + "?api-key=" + self.api_key + query_string
        if self.can_make_request():
            response = self.session.get(url)
            return response.json()

        return {"error": "Rate limit exceeded"}
