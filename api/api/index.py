import os
import sys
from flask import Flask, jsonify
from markupsafe import escape
import pandas as pd
from flask_cors import CORS

ruta_archivo_functions = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','functions.py'))
sys.path.append(os.path.dirname(ruta_archivo_functions))

ruta_archivo_mongo = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','mongo.py'))
sys.path.append(os.path.dirname(ruta_archivo_mongo))

from functions import upload_excel
from mongo import collection
import json

app = Flask(__name__)
cors = CORS(app)

@app.route("/auto/<string:id>")
def hello_world(id):
  return f"<h1>Hello {escape(id)}</h1>"

@app.route("/api/upload")
def upload():
  
  precios_excel, outpath_path, codigos = upload_excel()
  
  lineas_clean = [linea.replace('-','') for linea in codigos]
  
  prueba = [f"https://www.papelerabariloche.com.ar/img/p/{linea}/1.jpeg?quality=95&width=800&height=800&mode=max&upscale=false&format=webp" for linea in lineas_clean]
  
  precios_excel.insert(1,"Imagen",prueba)
    
  nuevas_columnas = ["codigo","imagen","articulo","costo","precio","fecha"]
  
  precios_excel.columns = nuevas_columnas

  #Limpiar columna fecha
  
  precios_excel["fecha"] = precios_excel["fecha"].astype(str)

  precios_excel["fecha"] = [fecha.replace("00:00:00","") for fecha in precios_excel["fecha"]]
  
  for x in precios_excel["fecha"]:
    print(type(x))
  
  data_dict = precios_excel.to_dict("records")
    
  collection.delete_many({})
  
  collection.insert_many(data_dict)
  
  precios_excel.drop("imagen", axis=1, inplace=True)
  
  #precios_excel.to_excel(outpath_path, index=False)
  
  return jsonify(precios_excel.to_json(orient="records"))
  #return send_file(outpath_path, as_attachment = True)

@app.route("/api/getall", methods=['GET'])
def getall():

  precios_excel = collection.find({})
  
  precios_excel_disc = [doc for doc in precios_excel]
  
  json_data = json.dumps(precios_excel_disc, default=str)
  
  return jsonify(json_data)
  
if __name__ == "__main__":
  app.run(debug=True)

