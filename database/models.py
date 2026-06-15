from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#SQLAlchemy instance - it will be initialized in app.py
db = SQLAlchemy()

class Deal(db.Model):
    """
    Travel Deal model mapped to the deals table.
    """

    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    travel_type = db.Column(db.String(50), nullable=False)


    def to_dict(self):
        """
        Converts the model object into a dictionary,
        so it can be easily sent as a JSON response using jsonify.
        """
        return {
            "id": self.id,
            "destination": self.destination,
            "price": self.price,
            "platform": self.platform,
            "rating": self.rating,
            "travel_type": self.travel_type
        }

class RecentlyViewed(db.Model):
    __tablename__ = "recently_viewed"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deals.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Deal er sathe relationship
    deal = db.relationship('Deal', backref='views')

    def to_dict(self):
        return {
            "id": self.deal.id,
            "destination": self.deal.destination,
            "price": self.deal.price,
            "platform": self.deal.platform,
            "rating": self.deal.rating,
            "travel_type": self.deal.travel_type,
            "viewed_at": self.viewed_at.strftime("%Y-%m-%d %H:%M:%S")
        }