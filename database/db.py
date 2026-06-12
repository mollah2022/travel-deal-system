class DealRepository:

    """
    This is an in-memory data store for Travel Deals.
    Later,we can replace it with a real database.
    if we keep the same methods,we will not need to change the service layer.
    """

    def __init__(self):
        self._deals = []        # list of deal dictionaries
        self._next_id = 1      #  auto-increment id counter

    def add_deal(self,deal_data):
        """
         Adds a new deal and returns the deal object with its id.
        """

        deal = {
            "id": self._next_id,
            "destination": deal_data["destination"],
            "price": deal_data["price"],
            "platform": deal_data["platfrom"],
            "rating": deal_data["rating"],
            "travel_type": deal_data["travel_type"]
        }

        self.deals.append(deal)
        self._next_id += 1
        return deal

    def get_all_deals(self):
        """
        Returns a list of all deals.
        """
        return self._deals
    
    def get_deal_by_id(self,deal_id):
        """
        Returns a deal by its id, or None if not found.
        """
        for deal in self._deals:
            if deal["id"] == deal_id:
                return deal
        return None

#one share instance.it will be imported and used in the service layer.

deal_repository = DealRepository()