import os
import sys
from flask import Flask, jsonify, request
from markupsafe import escape
import pandas as pd
from unidecode import unidecode
from flask_cors import CORS
from functions import clean_file
from mongo import collection
import json

app = Flask(__name__)
cors = CORS(app)

@app.route("/auto/<string:id>")
def hello_world(id):
  return f"<h1>Hello {escape(id)}</h1>"

@app.route("/api/upload", methods=["GET"])
def upload():
  cleaned_excel = clean_file()
  return jsonify(cleaned_excel.to_json(orient="records"))
  #return send_file(outpath_path, as_attachment = True)
  
@app.route("/api/manual_upload", methods=["POST"])
def manual_upload():
  if 'file' not in request.files:
      return jsonify({'error': 'No file part'}), 400

  file = request.files['file']
  cleaned_excel = clean_file(file)
  if file.filename == '':
      return jsonify({'error': 'No selected file'}), 400


  # Aquí puedes guardar el archivo en el sistema de archivos
  # Por ejemplo:
  # file.save('uploads/' + secure_filename(file.filename))

  return jsonify(cleaned_excel.to_json(orient="records"))
  
  
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
  df["ARTICULO"] = df["ARTICULO"].apply(unidecode)
  filtrados = df[df["ARTICULO"].str.contains(buscador, case=False)]
  print(filtrados)
  return jsonify(filtrados.to_json(orient='records', default_handler=str))  
  
if __name__ == "__main__":
  app.run(debug=True)

