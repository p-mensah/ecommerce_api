# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Connect to Mongo Atlas Cluster
# mongo_client = MongoClient(os.getenv("MONGO_URI"))

# # Access database
# ecommerce_db = mongo_client["ecommerce_db"]

# # Pick a collection to operate on
# events_collection = ecommerce_db["ecommerce"]

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    mongo_client = MongoClient(MONGO_URI)
    ecommerce_db = mongo_client["ecommerce"]
    products_collection = ecommerce_db["products"]
    users_collection = ecommerce_db["users"]
    carts_collection = ecommerce_db["carts"]
    orders_collection = ecommerce_db["orders"]
except ConnectionFailure as e:
    print(f"Error connecting to MongoDB: {e}")
