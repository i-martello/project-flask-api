from pymongo import MongoClient

client = MongoClient("mongodb+srv://First:nacho@personalcluster.hg1pfct.mongodb.net/Precios-CopyArt?retryWrites=true&w=majority")

db = client["Precios-CopyArt"]
collection = db["Precios"]