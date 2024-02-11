from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_KEY = os.environ.get("MONGO_KEY")
client = MongoClient(MONGO_KEY)

db = client["Precios-CopyArt"]
collection = db["Precios"]