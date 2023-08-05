from . import HTTP_CLIENT

class Company():
    """Class representing a company

    This class is a company, companies are object that can be saved and data such as statements,¨
    stock prices and more for them can be retreived.
    """
    def __init__(self, data):
        self.simId = str(data["simId"])
        self.name = data["name"]
        self.ticker = data["ticker"]

    def get_info(self):
        """Fetches info about the company

        Wrapper for https://simfin.com/api/v1/documentation/#operation/getCompById.
        This method uses one API call.

        Returns:
            dict: A dict with the information about the company.
        """
        response = HTTP_CLIENT.request("/companies/id/" + self.simId)
        if response:
            response["sectorCode"] = str(response["sectorCode"])
            response["simId"] = str(response["simId"])
            return response
        return None

    def statements(self):
        """Fetches all available statements for company

        Wrapper for https://simfin.com/api/v1/documentation/#operation/getCompStatementList.
        This method uses one API call.

        Returns:
            dict: Dict with lists for all balance, profif and loss and cash flow statements for
            the company.
        """
        response = HTTP_CLIENT.request("/companies/id/" + self.simId + "/statements/list/")
        return response

    def statement(self, statement, period="TTM", year=None, standardised=True):
        """Get a statement for the company

        Get a statement for a specific period for the company in original or standarised format.
        Wrapper for https://simfin.com/api/v1/documentation/#operation/getCompStatement and
        https://simfin.com/api/v1/documentation/#operation/getCompStatementStandardised. This method
        uses one API call.

        Args:
            statement: One of ``"pl"``, ``"bs"`` or ``"cf"`` representing what statement should be\
            fetched.
            period (str): One of ``"Q1"``, ``"Q2"``, ``"Q3"``, ``"Q4"``, ``"H1"``, ``"H2"``,\
            ``"9M"``, ``"FY`` or ``"TTM"`` representing the period you want the statement for. If\
            you choose ``"TTM"``, you can also specify an offset ranging from -0.25 to -10 in steps\
            of 0.25, the offset comes just after ``"TTM"`` to get older data. (default: ``"TTM"``)
            year (int): The year to retrieve data for (default: None)
            standardised (bool): (default: True)

        Returns:
            dict: Dict with the requested data plus metadata
        """
        query = {"stype": statement, "ptype": period, "fyear": year}
        if standardised:
            url = "/companies/id/" + self.simId +"/statements/standardised"
        else:
            url = "/companies/id/" + self.simId + "/statements/original"

        response = HTTP_CLIENT.request(url, query)
        return response

    def ratios(self, indicators=None):
        """Get TTM ratios for company

        Get all or some specified TTM financial ratios for the company. Wrapper for
        https://simfin.com/api/v1/documentation/#operation/getCompRatios. This method uses one API
        call.

        Args:
            indicators (list): list of indicators to retrieve. (default: None)

        Returns:
            list: dicts each representing one indicator.
        """
        query = {}
        if indicators:
            query["indicators"] = ",".join(indicators)
        response = HTTP_CLIENT.request("/companies/id/" + self.simId + "/ratios", query)
        return response

    def aggregated_shares(self, filter=None):
        """Get aggregated shares figure

        Get the aggregated shares outstanding figures, meaning that the figures are weighted sums
        of all share classes of the same type (common/preferred). Figures here are adjusted for
        share splits also. Wrapper for
        https://simfin.com/api/v1/documentation/#operation/getCompSharesAggregated. This method uses
        one API call.

        Args:
            filter (str): One optional of ``"common-outstanding"``, ``"common-outstanding-basic"``,
            ``"common-outstanding-diluted"``, ``"preferred"`` (default: None)

        Returns:
            list: dicts containing aggregated shares figure
        """
        if not filter:
            filter = ""
        query = {"filter": filter}
        response = HTTP_CLIENT.request("/companies/id/" + self.simId + "/shares/aggregated", query)
        return response

    def prices(self, start=None, end=None):
        """Get stock prices

        Retrieves share price data for the primary share class of the company between start and end.
        Wrapper for https://simfin.com/api/v1/documentation/#operation/getPrices. This method uses
        one API call.

        Args:
            start (date): Start date for price data, first available if ommitted. (default: None)
            end (date): End date for price data, last available if ommitted. (default: None)

        Returns:
            dict: share price data and metadata for the company.
        """
        query = {}
        if start:
            query["start"] = start.strftime("%Y-%m-%d")
        if end:
            query["end"] = end.strftime("%Y-%m-%d")

        response = HTTP_CLIENT.request("/companies/id/" + self.simId + "/shares/prices", query)
        return response

    def share_classes(self):
        """Get all share classes for company

        Get all the available share classes and metadata for them. Wrapper for
        https://simfin.com/api/v1/documentation/#operation/getCompSharesClassesList. This method
        uses one API call.

        Returns:
            list: list of dicts, one dict representing one share class.
        """
        response = HTTP_CLIENT.request("/companies/id/" + self.simId + "shares/classes/list")
        return response

    def outstanding_shares_for_class(self, share_class_id):
        """Get outstanding share figures for share class

        These are shares outstanding figures for single share classes. These figures are 'raw',
        meaning that they are not adjusted for share splits like the aggregated share figures (see
        above) and are also just available for the periods that have been reported by the company
        (the aggregated figures also contain calculated periods, such as Q4 which is often not
        reported seperately, because only full financial years figures are reported mostly).
        Wrapper for https://simfin.com/api/v1/documentation/#operation/getCompSharesClassesList.
        This method uses one API call.

        Args:
            share_class_id (str): id of the share class.

        Returns:
            dict: dict with shares outstanding figures for share class
        """
        url = "/companies/id/" + self.simId + "/shares/classes/" + share_class_id + "/outstanding"
        response = HTTP_CLIENT.request(url)
        return response

    def share_price_for_class(self, share_class_id, start=None, end=None):
        """Get share prices for share class

        Retrieves share price data for the primary share class of the company between start and end
        for the specified share class. Wrapper for
        https://simfin.com/api/v1/documentation/#operation/getPrices. This method uses one API call.

        Args:
            share_class_id (str): id of the share class.
            start (date): Start date for price data, first available if ommitted. (default: None)
            end (date): End date for price data, last available if ommitted. (default: None)

        Returns:
            dict: share price data and metadata for the share class.
        """
        query = {}
        if start:
            query["start"] = start.strftime("%Y-%m-%d")
        if end:
            query["end"] = end.strftime("%Y-%m-%d")
        url = "/companies/id/" + self.simId + "/shares/classes/" + share_class_id + "/prices"
        response = HTTP_CLIENT.request(url, query)
        return response
