from database.models import db, Deal, RecentlyViewed 
from collections import deque


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

    def search_deals(self,destination=None, platform=None, travel_type=None):
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

        if platform:
            query = query.filter(
                Deal.platform.ilike(f"%{platform}%")
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
    Recently viewed deals - SQLAlchemy diye database e save kore.
    Last 10 ta track kore, duplicate hole purana ta delete kore notun ta add kore.
    """

    def add(self, deal):
        """
        Deal ke recently viewed e add kore.
        Same deal already thakle age ta delete kore notun kore add kore.
        """
        # Duplicate check - same deal_id already ache kina, thakle delete koro
        existing = RecentlyViewed.query.filter_by(deal_id=deal["id"]).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # Notun entry add koro
        new_view = RecentlyViewed(deal_id=deal["id"])
        db.session.add(new_view)
        db.session.commit()

        # 10 er beshi thakle oldest ta delete koro
        total = RecentlyViewed.query.count()
        if total > 10:
            oldest = RecentlyViewed.query.order_by(
                RecentlyViewed.viewed_at.asc()
            ).first()
            db.session.delete(oldest)
            db.session.commit()

    def get_all(self):
        """
        Recently viewed deals return kore - most recent first.
        """
        recent = RecentlyViewed.query.order_by(
            RecentlyViewed.viewed_at.desc()
        ).all()
        return [r.to_dict() for r in recent]



# Single shared instance - it will be imported and used in the service layer.
deal_repository = DealRepository()
recently_viewed_repository = RecentlyViewedRepository()