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

    def search_deals(self,destinatuin=None, platform=None, travel_type=None):
        """
        Partial, case-insensitive search by destination, platform, travel_type.
        Returns: list of dict
        """

        query = Deal.query

        if destination:
            query = query.filter(
                Deal.destination.ilike(f"%{destination}%")
            )

        if travel_type:
            query = query.filter(
                Deal.travel_type.ilike(f"%{travel_type}%")
            )
        
        results = query.all()
        return [deal.to_dict() for deal in results]

    def filter_deals_by_price(self,min_price=None, max_price=None):
        """
        Filter deals by price range.
        Returns: list of dict
        """
        query = Deal.query

        if min_price is not None:
            query = query.filter(Deal.price >= min_price)

        if max_price is not None:
            query = query.filter(Deal.price <= max_price)

        
        results = query.all()
        return [deal.to_dict() for deal in results]

    def sort_deals(self, sort_by="price", order="asc"):
        """
        Sort deals by a given fiend and order.
        Return: list of dict
        """
        
        #get the column to sort by
        sort_column = getattr(Deal,sort_by)

        if order == "desc":
            sort_column = sort_column.desc()

        
        results = Deal.query.order_by(sort_column).all()
        return [deal.to_dict() for deal in results]


class RecentlyViewedRepository:
    """
    Tracks recently viewed deals (last 10, no duplicates).
    In-memory resets on server restart(intentional).
    """

    def add(self, deal):
        """
        Adds a deal to recently viewed list.
        If it already exists, remove it first and then add it again at the top.
        """
        # Check for duplicates - whether the same id already exists
        self._recent = deque(
            [d for d in self._recent if d["id"] != deal["id"]],
            maxlen=10
        )
        self._recent.append(deal)

    def get_all(self):
        """
        Returns recently viewed deals most recent first
        """

        return list(reversed(self._recent))
    


# Single shared instance - it will be imported and used in the service layer.
deal_repository = DealRepository()
recently_viewed_respository = RecentlyViewedRepository()