from flask import Flask
from markupsafe import escape
import pandas as pd
from flask_cors import CORS
from functions import upload_excel
app = Flask(__name__)
CORS(app)

@app.route("/auto/<string:id>")
def hello_world(id):
  return f"<h1>Hello {escape(id)}</h1>"

@app.route("/api/upload", methods=['POST'])
def upload():
  
  precios_excel, outpath_path = upload_excel()
  
  precios_excel.to_excel(outpath_path, index=False)

  return ''
  
if __name__ == "__main__":
  app.run(debug=True)

