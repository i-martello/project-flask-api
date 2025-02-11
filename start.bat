@echo off

:: Iniciar el cliente
start cmd /k "cd client && npm run dev"

:: Iniciar el servidor de Python
cd api
call venv\Scripts\activate
python index.py
