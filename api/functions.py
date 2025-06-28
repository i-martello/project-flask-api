import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from mongo import collection

load_dotenv()

def limpiar_codigos_txt(path='codigos.txt') -> list[str]:
    """Lee el archivo y devuelve una lista de códigos únicos y limpios."""
    with open(path, 'r') as archivo:
        codigos = [linea.strip() for linea in archivo.readlines()]
    codigos_unicos = sorted(set(codigos))  # opcional: sorted para ordenarlos
    with open(path, 'w') as archivo:
        archivo.write('\n'.join(codigos_unicos))
    return codigos_unicos

def cargar_y_filtrar_excel(manual_excel, codigos) -> tuple[pd.DataFrame, str, list[str]]:
    """Carga el Excel, filtra por códigos, redondea precios, y devuelve el DataFrame."""
    df = pd.read_excel(manual_excel, skiprows=9)
    df = df.drop(df.columns[[0, 5, 6, 7, 8]], axis=1)
    df["PRECIO CON IVA"] = df["PRECIO CON IVA"].round()

    df_filtrado = df[df["CÓDIGO"].isin(codigos)].copy()
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"precios_{fecha_actual}"

    return df_filtrado, filename, df_filtrado["CÓDIGO"].tolist()

def upload_excel(manual_excel):
    codigos = limpiar_codigos_txt()
    return cargar_y_filtrar_excel(manual_excel, codigos)

def clean_file(manual_file=False):
    df, output_path, codigos = upload_excel(manual_file)

    # Generar URLs de imágenes
    codigos_limpios = [codigo.replace('-', '') for codigo in codigos]
    urls_imagen = [
        f"https://www.papelerabariloche.com.ar/img/p/{codigo}/1.jpeg?quality=95&width=800&height=800&mode=max&upscale=false&format=webp"
        for codigo in codigos_limpios
    ]

    # Renombrar y agregar columnas
    df.rename(columns={
        "CÓDIGO": "CODIGO",
        "DESCRIPCIÓN": "ARTICULO",
        "PRECIO CON IVA": "COSTO 21%",
        "PRECIO OFERTA": "OFERTA"
    }, inplace=True)

    df.insert(1, "IMAGEN", urls_imagen)
    df["COSTO 10.5%"] = (df["COSTO 21%"] / 1.21 * 1.105).round()
    df["VENTA"] = (df["COSTO 21%"] * 1.5).round()
    df["DTO"] = (df["COSTO 10.5%"] * 1.5).round()

    # Eliminar columnas no necesarias
    if "OFERTA" in df.columns:
        df.drop(columns=["OFERTA"], inplace=True)
    if "IMAGEN" in df.columns:
        df.drop(columns=["IMAGEN"], inplace=True)
    if len(df.columns) > 8:
        df.drop(columns=[df.columns[8]], inplace=True)  # Columna "DESCUENTO POR CANTIDAD"

    # Subida a MongoDB
    collection.delete_many({})
    collection.insert_many(df.to_dict(orient="records"))

    return df
