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
    
#single shared instance this instance will be used in the routes.
deal_service = DealService()