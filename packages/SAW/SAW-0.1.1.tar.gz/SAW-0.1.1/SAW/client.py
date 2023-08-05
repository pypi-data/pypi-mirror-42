from . import HTTP_CLIENT
from .company import Company

class Client():
    """Main API client

    Client used to setup connection and retrieve companies and database changes from the API.
    """
    def __init__(self, api_key, simfin_plus=False):
        HTTP_CLIENT.set_api_key(api_key, simfin_plus)

    @staticmethod
    def get_company_by_ticker(ticker):
        """Get a company by its ticker

        Returns a single comapny https://simfin.com/api/v1/documentation/#tag/Company. This method
        uses one API call.

        Args:
            ticker (str): Ticker of the company

        Returns:
            Company: The company with specified ticker, None if no company with ticker
        """
        response = HTTP_CLIENT.request("/info/find-id/ticker/" + ticker)
        if response:
            return Company(response[0])

        return None

    @staticmethod
    def get_companies_by_name(name):
        """Find company by name

        Fetches all companies when searching by name. Wrapper for
        https://simfin.com/api/v1/documentation/#operation/getIdByName. This method uses one API
        call.

        Args:
            name (str): Company name to search by

        Returns:
            list: List with zero to multiple elements of type :class:`Company`.
        """
        response = HTTP_CLIENT.request("/info/find-id/name-search/" + name)
        companies = []
        for company in response:
            companies.append(Company(company))

        return companies

    @staticmethod
    def get_all_companies():
        """Get all companies

        Gets all available companies in the simfin database. This method uses one API call.

        Returns:
            list: List with multiple elements of type :class:`Company`
        """
        response = HTTP_CLIENT.request("/info/all-entities")
        companies = []
        for company in response:
            companies.append(Company(company))

        return companies

    @staticmethod
    def get_changes(start=None, end=None, filter=None, simId=None,
                    results_per_page=50, current_page=1):
        """Get all changes to the database

        Gets all changes done to the SimFin database, in specified timeframe with specified filtes.
        This method uses one API call.

        Args:
            start (datetime): start datetime of changes, timezone is UTC  (default: None)
            end (datetime): end datetime of changes, timezone is UTC (default: None)
            filter (str): ``"d-add"``, ``"d-chg"``, ``"d-del"``, ``"c-new"`` or ``"c-del"``. Can\
            also be seperated by commas to filter for many events. (default: None)
            simId (str): SimFin ID to filter for (default: None)
            results_per_page (int): company SimFin ID to use as filter (default: 50)
            current_page (int): current page (default: 1)

        Returns:
            dict: all changes done with filters applied
        """
        query = {}
        if start:
            query["start"] = start.strftime("%Y-%m-%d_%H:%M:%S")
        if end:
            query["end"] = end.strftime("%Y-%m-%d_%H:%M:%S")
        if filter:
            query["filter"] = filter
        if simId:
            query["simId"] = simId
        if results_per_page:
            query["results-per-page"] = str(results_per_page)
        if current_page:
            query["current-page"] = str(current_page)

        response = HTTP_CLIENT.request("/info/changes", query)
        for i in range(len(response["changes"])):
            response[i]["simId"] = str(response[i]["changes"])

        return response

    @staticmethod
    def get_rate_limit():
        """Get current rate limit

        Get the amount of api calls left to used.

        Returns:
            int: Current amount of api calls left to used as integer
        """
        return HTTP_CLIENT.tokens
