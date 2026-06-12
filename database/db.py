from database.models import db, Deal


class DealRepository:
    """
    Travel Deal database operations are handled using SQLAlchemy ORM.  
    The method names are kept the same (add_deal, get_all_deals, get_deal_by_id)  
    so that no changes are needed in the service layer.
    """

    def add_deal(self, deal_data):
        """
        Adds a new deal and returns the deal dict with its id.
        """
        new_deal = Deal(
            destination=deal_data["destination"],
            price=deal_data["price"],
            platform=deal_data["platform"],
            rating=deal_data["rating"],
            travel_type=deal_data["travel_type"]
        )

        db.session.add(new_deal)
        db.session.commit()

        return new_deal.to_dict()

    def get_all_deals(self):
        """
        Returns a list of all deals.
        """
        all_deals = Deal.query.all()
        return [deal.to_dict() for deal in all_deals]

    def get_deal_by_id(self, deal_id):
        """
        Returns a deal dict by its id, or None if not found.
        """
        deal = Deal.query.get(deal_id)

        if deal is None:
            return None

        return deal.to_dict()


# Single shared instance - it will be imported and used in the service layer.
deal_repository = DealRepository()