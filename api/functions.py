import io
import requests
from flask import Flask, request, jsonify
from mongo import collection
from markupsafe import escape
import pandas as pd
from flask_cors import CORS
import datetime

def upload_excel():  
  def excel(codigos):
    url = "https://www.papelerabariloche.com.ar/lista-precios" 
    cookies = {"SofMic.Shops.PapeleraBariloche.Web.Auth": "8CB1A761993276169AD63CD164B07D594166CB8E139FB463EB6CECB299895743663FB02FFB83A8CE0A9FF8643EBC3120064D4BE2569B90AAB76B548A20176C0F22C8BDF8E3172978245202B557100D818212AE13595DD54FBF57C527DE24AF80AABB9E5DB5577C4C74D2340F72A708ED6E2B4EAF21C35DB2E1B153C3B4864530"}
    response = requests.get(url, cookies=cookies) 
    contenido_excel = response.content 
    df_excel = pd.read_excel(io.BytesIO(contenido_excel), skiprows=9)  
    df_excel = df_excel.drop(df_excel.columns[[0,5,6,7,8]], axis=1)
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    outpath_path = f"precios_{fecha_actual}.xlsx"
    df_excel["PRECIO CON IVA"] =  [round(x) for x in df_excel["PRECIO CON IVA"].to_list()]
    codigos_limpios = list(set(codigos))
    filas_filtradas = df_excel[df_excel["CÓDIGO"].isin(codigos_limpios)]
    codigos_excel = filas_filtradas["CÓDIGO"].to_list()
    columnas = [round(x) for x in filas_filtradas["PRECIO CON IVA"].to_list()]
    filas_filtradas.insert(3, "Precio", [round(x * 1.5) for x in columnas] )
    
    return filas_filtradas, outpath_path,codigos_excel 
    # json =  filas_filtradas.to_json(orient='records')
    # filas_filtradas.to_excel(outpath_path, index=False)

  with open('./codigos.txt') as txt_file:
    lineas_sin_limpiar = txt_file.readlines()
    lineas_txt = [linea.strip() for linea in lineas_sin_limpiar]
    json_excel = excel(lineas_txt)     
  
  return json_excel   


def clean_file():
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
  
  return precios_excel
  
  #precios_excel.to_excel(outpath_path, index=False)
  
  
  #return send_file(outpath_path, as_attachment = True)