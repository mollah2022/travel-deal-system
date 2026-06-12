from flask_sqlalchemy import SQLAlchemy


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