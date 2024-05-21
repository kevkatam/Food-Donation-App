"""
configuration module
"""

class Config:
    """
    configuration class for the application
    Contains all the necessary configurations for the application, including
    email server settings and MongoDB connection URI
    Attributes:
        MAIL_SERVER: The mail server address for sending emails
        MAIL_PORT: The port number to use for the mail server
        MAIL_USE_TLS: Whether to use TLS(Transport Layer Security) for the
                      mail server connection.
        MAIL_PASSWORD: The password for authenticating with the mail server.
        MONGO_URI: The URI for connecting to the MongoDB database.
    """
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kyalokimeu0@gmail.com'
    MAIL_PASSWORD = 'Alcatraz12!'    
    MONGO_URI = "mongodb://localhost:27017/mydatabase"
