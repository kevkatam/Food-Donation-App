from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """
    Initialize the MongoDB connection with the Flask app

    Args:
        app (Flask): The Flask application instance.

    Returns:
        PyMongo: The initialized PyMongo instance.
    """
    mongo.init_app(app)
    return mongo
