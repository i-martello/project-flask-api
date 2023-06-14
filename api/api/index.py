import os
import sys
from flask import Flask, jsonify, request
from markupsafe import escape
import pandas as pd
from unidecode import unidecode
from flask_cors import CORS

ruta_archivo_functions = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','functions.py'))
sys.path.append(os.path.dirname(ruta_archivo_functions))

ruta_archivo_mongo = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','mongo.py'))
sys.path.append(os.path.dirname(ruta_archivo_mongo))

from functions import clean_file
from mongo import collection
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins:": "https://precioscopyart.vercel.app"}})

@app.route("/auto/<string:id>")
def hello_world(id):
  return f"<h1>Hello {escape(id)}</h1>"

@app.route("/api/upload", methods=["POST"])
def upload():
  cleaned_excel = clean_file()
  return jsonify(cleaned_excel.to_json(orient="records"))
  #return send_file(outpath_path, as_attachment = True)
  
@app.route("/api/uploadlist", methods=["GET"])
def list():
  cleaned_excel = clean_file()
  data_dict = cleaned_excel.to_dict("records")
  collection.delete_many({})
  collection.insert_many(data_dict)
  return ''

@app.route("/api/getall", methods=['GET'])
def getall():

  precios_excel = collection.find({})
  
  precios_excel_disc = [doc for doc in precios_excel]
  
  json_data = json.dumps(precios_excel_disc, default=str)
  
  return jsonify(json_data)

@app.route("/api/search", methods=['GET'])
def search():
  buscador = request.args.get("search")
  
  precios_excel = collection.find({})
  precios_excel_disc = [doc for doc in precios_excel]
  df = pd.DataFrame(precios_excel_disc)
  df["articulo"] = df["articulo"].apply(unidecode)
  filtrados = df[df["articulo"].str.contains(buscador, case=False)]
  print(filtrados)
  return jsonify(filtrados.to_json(orient='records', default_handler=str))  
  
if __name__ == "__main__":
  app.run(debug=True)

