from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_KEY = os.environ.get("MONGO_KEY")
client = MongoClient(MONGO_KEY)

try:
    # Verificamos la conexión listando las bases de datos
    db = client["Precios-CopyArt"]
    collection = db["Precios"]
    print("Conexión exitosa a la base de datos")

except Exception as e:
    print("Error de conexión:", e)