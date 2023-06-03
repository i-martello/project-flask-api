from flask import Flask, request, jsonify
from markupsafe import escape
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/auto/<string:id>")
def hello_world(id):
  return f"<h1>Hello {escape(id)}</h1>"

@app.route("/api/upload", methods=['POST'])
def upload():
  
  def excel(codigos):
    file_excel = request.files['file']
    df_excel = pd.read_excel(file_excel, skiprows=9)  
    df_excel = df_excel.drop(df_excel.columns[[0,5,6,7,8]], axis=1)
    outpath_path = "bariloche_excel.xlsx"
    df_excel["PRECIO CON IVA"] =  [round(x) for x in df_excel["PRECIO CON IVA"].to_list()]
    filas_filtradas = df_excel[df_excel["CÓDIGO"].isin(codigos)]
    columnas = [round(x) for x in filas_filtradas["PRECIO CON IVA"].to_list()]
    
    
    filas_filtradas.insert(3, "Precio", [round(x * 1.5) for x in columnas] )
    
    # json =  filas_filtradas.to_json(orient='records')
    filas_filtradas.to_excel(outpath_path, index=False)
    # return json

  with open('./codigos.txt') as txt_file:
    lineas_sin_limpiar = txt_file.readlines()
    lineas_txt = [linea.strip() for linea in lineas_sin_limpiar]
    json_excel = excel(lineas_txt)     
  
  return jsonify(json_excel)      

if __name__ == "__main__":
  app.run(debug=True)

