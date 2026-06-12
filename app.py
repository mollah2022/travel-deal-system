from flask import Flask

def create_app():
    """
    This is an Application Factory function.
    Here we create the Flask app
    After that we will register blueprints(routes) in this app
    """
    app = Flask(__name__)

    @app.route('/')
    def health_check():
        return {
            "status":"success",
            "message":"Travel Deal Management System is running!"
        }, 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)