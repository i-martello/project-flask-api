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
    cookies = {"SofMic.Shops.PapeleraBariloche.Web.Auth": "B0FD06C9854E7BB1CFB1421807CD1A76D47429FA6C2C0D204D924C8586335DB6F62C3CF57C098DD27667BEAFBB350C7E456C7C180E06BB96A3AD362D8799B10B171FC416E460383B456ACA2EBB29EDAB45701E2ED79360822FF6E15D682B712A382E30F5D3687DBDE33E4BC6B6B2810E46E6ABC3F35A341845280239A7CFBF14"}
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
  precios_excel.rename(columns={"CÓDIGO":"CODIGO"},inplace=True)
  precios_excel.insert(1,"imagen",prueba)
  precios_excel.rename(columns={"PRECIO CON IVA":"c_iva"}, inplace=True)
  precios_excel.rename(columns={"DESCRIPCIÓN":"ARTICULO"}, inplace=True)
  precios_excel.insert(4,"COSTO",[round(c_iva/ 1.21 * 1.105) for c_iva in precios_excel["c_iva"]  ])
  precios_excel.insert(5,"VENTA",[round(c_iva* 1.5) for c_iva in precios_excel["c_iva"] ])
  precios_excel.insert(6,"DTO",[round(costo* 1.5) for costo in precios_excel["COSTO"]])  
  precios_excel.rename(columns={"FECHA ULTIMA ACTUALIZACIÓN": "FECHA"}, inplace=True)
  precios_excel["FECHA"] = precios_excel["FECHA"].astype(str)
  precios_excel["FECHA"] = [fecha.replace("00:00:00","") for fecha in precios_excel["FECHA"]]
  
  #Limpiar columna fecha

  data_dict = precios_excel.to_dict("records")
  collection.delete_many({})
  collection.insert_many(data_dict)
  
  precios_excel.drop("imagen", axis=1, inplace=True)
  
  precios_excel.rename(columns={"c_iva":"C/IVA"}, inplace=True)
  
  return precios_excel
  
  #precios_excel.to_excel(outpath_path, index=False)
  
  
  #return send_file(outpath_path, as_attachment = True)