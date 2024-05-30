from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB conncetion details
MONGO_DETAILS = "mongodb+srv://kyalokimeu0:vhxyh4oRxn2Mc7De@cluster0.tzweqoz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Establish connection to MongoDB server
client = AsyncIOMotorClient(MONGO_DETAILS)

# Initialize database
database = client.food_donation

# Initialize collections for storing data
donor_collection = database.get_collection("donors")
recipient_collection = database.get_collection("recipients")
donation_collection = database.get_collection("donations")
user_collection = database.get_collection("users")
review_collection = database.get_collection("reviews")
