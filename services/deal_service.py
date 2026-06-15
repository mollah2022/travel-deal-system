from database.db import deal_repository
from utils.validators import validate_deal_data

class DealService:
    """
    All travel deal related business logic will be inside this class.
    Routes will only call the methods of this service.
    """

    def create_deal(self,data):
        """
        Create a new deal.
        returns:
        1.deal(dictionary) or None
        2.error(dictionary) or None
        """

        #step-1 : validate input data
        is_valid,errors = validate_deal_data(data)

        if not is_valid:
            return None, {"error":errors}

        #step-2 : save to database (repository)
        deal = deal_repository.add_deal(data)

        return deal,None

    def get_all_deals(self):
        """
        Returns the list of all deals
        Returns: a list of dictionaries.
        """

        return deal_repository.get_all_deals()

    def get_deal_by_id(self,deal_id):
        """
        Finds and returns a single deal by ID.
        Returns:
        1.deal(dictionary) or None
        2.error(dictionary) or None
        """

        deal = deal_repository.get_deal_by_id(deal_id)

        if deal is None:
            return None,{"errors":[f"Deal with is {deal_id} not found."]}

        return deal,None
    
    def search_deals(self, params):
        """
        Searches deals using query parameters.
        Returns: (results: list or None, error: dict or None)
        """

        logger.info(f"Search request recived - params:{params}")

        is_valid, errors = validate_search_params(params)

        if not is_valid:
            logger.worning(f"Search validation failed - errors: {errors}")
            return None, {"errors":errors}
        
        destination = params.get("destination", "").strip()
        platform = params.get("platform", "").strip()
        travel_type = params.get("travel_type", "").strip()


        if not resilts:
            logger.info(f"Search returned no results - params: {params}")
        else:
            logger.info(f"Search successful - {len(results)} result(s) found")

        return results, None

    def filter_deals(self, params):
        """
        Filters deals by price range.
        Returns: (results: list or None, error: dict or None)
        """

        logger.info(f"Filter request recived - params: {params}")
        
        is_valid, errors = validate_filter_params(params)

        if not is_valid:
            logger.warning(f"Filter validation failed - errors : {errors}")
            return None, {"errors": errors}

        min_price = float(params["min_price"]) if params.get("min_price") else None
        max_price = float(params["max_price"]) if params.get("max_price") else None

        results = deal_repository.filter_deals_by_price(
            min_price = min_price,
            max_price = max_price
        )

        logger,info(f"Filter successfull - {len(results)} result(s) found")
        return results, None

    def sort_deals(self, params):
        """
        Sorts deals by the specified field and order.
        Returns: (results: list or None, error: dict or None)
        """

        logger.info(f"Sort request recived - params: {params}")

        is_valid, errors = validate_sort_params(params)

        if not is_valid:
            logger.warning(f"sort validation failed - errors: {errors}")
            return None, {"errors":errors}

        sort_by = params.get("sort_by", "price").strip()
        order = params.get("order", "asc").strip().lower()

        results = deal_repository.sort_deals(sort_by=sort_by, order=order)

        logger.info(f"Sort successful - sorted by '{sort_by}' ({order}), {len(results)} result(s)")
        return results, None

        def get_recently_viewed(self):
            """
            Returns recently viewed deals.
            Returns: list of dict
            """

            recent = recently_viewed_repository.get_all()
            logger.info(f"Recently viewed deals fetched - total : {len(recent)}")
            return recent



#single shared instance this instance will be used in the routes.
deal_service = DealService()