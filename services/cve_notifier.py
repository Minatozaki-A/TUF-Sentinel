# Consulta de la API de NVD
import requests
from dotenv import load_dotenv
import logging
import os

load_dotenv()
api_key = os.getenv("API_KEY")

URL = "https://services.nvd.nist.gov/rest/json/cpes/2.0?cpeNameId="+api_key


response = requests.get(URL)
if response.status_code == 200:
    logging.info("CVEs notificadas")
    print('Data:', response.json())
else:
    print('Error en la solicitud, detalles:', response.text)
