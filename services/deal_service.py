from database.db import deal_repository, recently_viewed_repository, stats_repository
from utils.validators import (
    validate_deal_data,
    validate_search_params,
    validate_filter_params,
    validate_sort_params,
    validate_update_data
)
from utils.logger import logger

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

        # Recently viewed e add kora
        recently_viewed_repository.add(deal)
        logger.info(f"Deal fetched successfully - ID: {deal_id}")

        return deal,None
    
    def update_deal(self, deal_id, data):
        """
        updates an existing deal after validation.
        Returns: (deal: dict or None, error: dict or None)
        """

        #step 1: validate using same rules as create
        is_valid, errors = validate_update_data(data)

        if not is_valid:
            logger.warning(f"Update failed for deal ID {deal_id}")
            return None, {"errors": errors}

        #step 2: check deal exists, then update
        updated_deal = deal_repository.update_deal(deal_id, data)

        if updated_deal is None:
            logger.warning(f"Update failed - deal ID {deal_id} not found.")
            return None, {"errors": [f"Deal with id {deal_id} not found"]}

        logger.info(f"Deal update successfully - ID {deal_id}")
        return updated_deal, None

    def delete_deal(self, deal_id):
        """
        Deletes a deal by id.
        Returns: (success: bool, error: dict or None)
        """

        deleted = deal_repository.delete_deal(deal_id)

        if not deleted:
            logger.warning(f"Delete failed - deal ID {deal_id} not found")
            return False, {"errors": [f"Deal with id {deal_id} not found"]}


        logger.info(f"Deal deleted successfully - ID: {deal_id}")
        return True, None

    def search_deals(self, params):
        """
        Searches deals using query parameters.
        Returns: (results: list or None, error: dict or None)
        """

        logger.info(f"Search request recived - params:{params}")

        is_valid, errors = validate_search_params(params)

        if not is_valid:
            logger.warning(f"Search validation failed - errors: {errors}")
            return None, {"errors":errors}
        
        destination = params.get("destination", "").strip()
        platform = params.get("platform", "").strip()
        travel_type = params.get("travel_type", "").strip()

        # Log search keyword for "most searched destination" stats
        if destination:
            stats_repository.log_search(destination)

        results = deal_repository.search_deals(
            destination=destination or None,
            platform=platform or None,
            travel_type=travel_type or None
        )


        if not results:
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

        logger.info(f"Filter successfull - {len(results)} result(s) found")
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
        logger.info(f"Recently viewed deals fetched - total: {len(recent)}")
        return recent

    def get_popular_deals(self, limit=5):
        """
        Returns the most viewed deals.
        Returns: list of dict
        """

        popular = recently_viewed_repository.get_most_viewed(limit=limit)
        logger.info(f"Popular deals fetched total: {len(popular)}")
        return popular

class StatsService:
    """
    Handles API usage statistics business logic.
    kept separate from DealService for single responsibility
    stats are about the API itself, not about deals.
    """

    def get_stats(self):
        """
        Returns overall API usage statics.
        """

        stats = stats_repository.get_stats()
        logger.info(f"API stats fetched total requests: {stats['total_requests']}")
        return stats
        
#single shared instance this instance will be used in the routes.
deal_service = DealService()
stats_service = StatsService()