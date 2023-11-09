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
<<<<<<< HEAD
    cookies = {"SofMic.Shops.PapeleraBariloche.Web.Auth": "B8F98179864CE94F7B748587F7F94DDD737D6550CB142053C9EAE3091D5E653ED30E2040BCF7F1979AA508221C0387C3E172C2970ED76131E7ECECEE617ED816F57A33A569B3D70124DEBDAC4FA7F2AAB9C68B87735CF4969EED882F7D19DDD77F0AE3DB50D2875F599DDD54C85270B86D56339F79CB7BD7C0A790D8D76076DA"}
=======
    cookies = {"SofMic.Shops.PapeleraBariloche.Web.Auth": "0013F2709633AB52B69C69E37EF2862425CCC05C31ACB7489AC6AE9BD73307DED597B2DC723432FB6B4F35D70E87220978E2124B02A0F0DE11C5EBFB5E5D596F7451AB05BA961E06D0BE0AE8625BAD2F140424C4AFBD8969FA21F7339EAADE79A57B02AD26D038FF144AE8A8B3D390658B2115715A1EA4943FAB564D3AF30FC2"}
>>>>>>> c33d5a7962f5348b2940a4f037016152e84e6067
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