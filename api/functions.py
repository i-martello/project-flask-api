import io
import datetime
import os
import requests
from flask import jsonify
import urllib.parse
import httpx
from mongo import collection
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

PB_NAME = os.environ.get("NAME")
PB_PASSWD = os.environ.get("PASSWD")
PB_COOKIE = os.environ.get("COOKIE")

def upload_excel(manual_excel):  
  def excel(codigos):
    if not manual_excel:
      
      url = "https://www.papelerabariloche.com.ar/ingreso"

      headers = {
          "Host": "www.papelerabariloche.com.ar",
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.5",
          "Accept-Encoding": "gzip, deflate, br",
          "Content-Type": "application/x-www-form-urlencoded",
          "Origin": "https://www.papelerabariloche.com.ar",
          "Referer": "https://www.papelerabariloche.com.ar/ingreso",
          "Upgrade-Insecure-Requests": "1",
          "Sec-Fetch-Dest": "document",
          "Sec-Fetch-Mode": "navigate",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Fetch-User": "?1",
          "Te": "trailers"
      }

      data = {
          "frmLoginSubmitted": "1",
          "txtUsername": PB_NAME,
          "txtPassword": PB_PASSWD
      }

      response = httpx.post(url, headers=headers, data=data)

      # Imprimir el contenido de la respuesta y las cookies
      cookies = response.cookies

      # Imprimir el contenido de la respuesta y las cookies
      cookie_value = cookies.get(PB_COOKIE)
  
      url = "https://www.papelerabariloche.com.ar/lista-precios" 
      cookies = {PB_COOKIE: cookie_value}
      try:
        response = requests.get(url, cookies=cookies)
        print("acceso a pb exitoso")
      except:
        return jsonify({'error': 'No se pudo acceder a pb'}), 400
      contenido_excel = response.content 
      df_excel = pd.read_excel(io.BytesIO(contenido_excel), skiprows=9)  
    else:
      df_excel = pd.read_excel(manual_excel, skiprows=9)

    df_excel = df_excel.drop(df_excel.columns[[0,5,6,7,8]], axis=1)
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    outpath_path = f"precios_{fecha_actual}.xlsx"
    df_excel["PRECIO CON IVA"] =  [round(x) for x in df_excel["PRECIO CON IVA"].to_list()]
    codigos_limpios = list(set(codigos))
    filas_filtradas = df_excel[df_excel["CÓDIGO"].isin(codigos_limpios)]
    codigos_excel = filas_filtradas["CÓDIGO"].to_list()
    print(codigos_excel)
    return filas_filtradas, outpath_path,codigos_excel 
    # json =  filas_filtradas.to_json(orient='records')
    # filas_filtradas.to_excel(outpath_path, index=False)

  with open('./codigos.txt') as txt_file:
    lineas_sin_limpiar = txt_file.readlines()
    lineas_txt = [linea.strip() for linea in lineas_sin_limpiar]
    json_excel = excel(lineas_txt)     
  
  return json_excel   


def clean_file(manual_file = False):
  try:
    precios_excel, outpath_path, codigos = upload_excel(manual_file)
  except:
    return "error"
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
  
  #Limpiar columna fecha

  data_dict = precios_excel.to_dict("records")
  collection.delete_many({})
  collection.insert_many(data_dict)
  
  precios_excel.drop("imagen", axis=1, inplace=True)
  precios_excel.drop("FECHA", axis=1, inplace=True)

  
  precios_excel.rename(columns={"c_iva":"COSTO 21%"}, inplace=True)
  precios_excel.rename(columns={"COSTO":"COSTO 10.5%"}, inplace=True)
  
  return precios_excel
  
  #precios_excel.to_excel(outpath_path, index=False)
  
  
  #return send_file(outpath_path, as_attachment = True)