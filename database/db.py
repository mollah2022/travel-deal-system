from database.models import db, Deal, RecentlyViewed, ApiStat, SearchLog
from collections import deque
from sqlalchemy import func

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

    def update_deal(self, deal_id, deal_data):
        """
        update an existing deal with new data.
        Returns: updated deal dict, or None if not found.
        """
        deal = Deal.query.get(deal_id)
        if deal is None:
            return None

        deal.destination = deal_data["destination"]
        deal.price = deal_data["price"]
        deal.platform = deal_data["platform"]
        deal.rating = deal_data["rating"]
        deal.travel_type = deal_data["travel_type"]

        db.session.commit()
        return deal.to_dict()

    def delete_deal(self, deal_id):
        """
        Deletes a  deal by id.
        Returns: True if deleted, False if not found.
        """

        deal = Deal.query.get(deal_id)
        if deal is None:
            return None
        
        db.session.delete(deal)
        db.session.commit()
        return True

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

    def get_most_viewed(self, limit=5):
        """
        Returns deals ordered by how many times they were viewed.
        Uses all time view records (not just the last 10).
        """

        results = (
            db.session.query(
                RecentlyViewed.deal_id,
                func.count(RecentlyViewed.deal_id).label("view_count")
            )

            .group_by(RecentlyViewed.deal_id)
            .order_by(func.count(RecentlyViewed.deal_id).desc())
            .limit(limit)
            .all()
        )

        popular_deals = []
        for deal_id, view_count in results:
            deal = Deal.query.get(deal_id)
            if deal:
                deal_dict = deal.to_dict()
                deal_dict["view_count"] = view_count
                popular_deals.append(deal_dict)

        return popular_deals


class StatsRepository:
    """
    Tracks API usage statistics and search activity.
    """

    def _get_or_create_stat_row(self):
        """
        Internal helper - ensures a single ApiStat row always exists.
        """
        stat = ApiStat.query.first()
        if stat is None:
            stat = ApiStat(total_requests=0, successful_requests=0, failed_requests=0)
            db.session.add(stat)
            db.session.commit()
        return stat

    def record_request(self, success=True):
        """
        Increments total/successful/failed request counters.
        """
        stat = self._get_or_create_stat_row()
        stat.total_requests += 1
        if success:
            stat.successful_requests += 1
        else:
            stat.failed_requests += 1
        db.session.commit()

    def log_search(self, destination):
        """
        Records a search keyword for "most searched destination" stats.
        """
        if destination:
            entry = SearchLog(destination=destination.lower())
            db.session.add(entry)
            db.session.commit()

    def get_most_searched_destination(self):
        """
        Returns the most frequently searched destination, or None.
        """
        result = (
            db.session.query(
                SearchLog.destination,
                func.count(SearchLog.destination).label("count")
            )
            .group_by(SearchLog.destination)
            .order_by(func.count(SearchLog.destination).desc())
            .first()
        )
        if result is None:
            return None
        return {"destination": result[0], "search_count": result[1]}

    def get_stats(self):
        """
        Returns full API usage statistics.
        """
        stat = self._get_or_create_stat_row()
        data = stat.to_dict()
        data["most_searched_destination"] = self.get_most_searched_destination()
        return data

  

# Single shared instance - it will be imported and used in the service layer.
deal_repository = DealRepository()
recently_viewed_repository = RecentlyViewedRepository()
stats_repository = StatsRepository()