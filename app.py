from flask import Flask, jsonify
from routes.deal_routes import deal_bp
from database.models import db
from routes.stats_routes import stats_bp
from database.db import stats_repository

def create_app():
    """
    This is an Application Factory function.
    Here we create the Flask app
    After that we will register blueprints(routes) in this app
    """
    app = Flask(__name__)

    # ---------- Database Configuration ----------
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel_deals.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with this app
    db.init_app(app)


    # Create tables if they don't exist (runs inside app context)
    with app.app_context():
        db.create_all()


    #Register Blueprint
    app.register_blueprint(deal_bp)
    app.register_blueprint(stats_bp) 

    @app.route('/')
    def health_check():
        return {
            "status":"success",
            "message":"Travel Deal Management System is running!"
        }, 200


    # ---------- Request Tracking Middleware ----
    @app.after_request
    def track_api_stats(response):
        """
        Runs after every request. Automatically records whwther
        the request was successful or failed
        """
    
        is_success = response.status_code < 400
        stats_repository.record_request(success=is_success)
        return response



    # ---------- Global Error Handlers ----------

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "The requested resource was not found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "message": "This HTTP method is not allowed for this endpoint."
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "message": "Bad request. Please check your input."
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Something went wrong on the server. Please try again later."
        }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)