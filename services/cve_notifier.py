# Consulta de la API de NVD
import requests
from dotenv import load_dotenv
import logging
import os
import time

load_dotenv()
API_KEY=os.getenv("API_KEY")




class NVDApiClient:
    def __init__(self, api_key):
        self.base_url = "https://services.nvd.nist.gov/rest/json/cpes/2.0?"
        self.headers = {"apiKey": api_key}
        # Con API Key, el límite es ~50 peticiones cada 30 segundos.
        # Un delay de 0.6s entre llamadas es seguro.
        self.delay = 0.6

    def get_vulnerabilities(self, cpe_name):
        params = {"keywordSearch": cpe_name,
                    "resultsPerPage": 20}
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print("Error: Posible baneo temporal o API Key inválida.")
            else:
                print(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")

        time.sleep(self.delay)
        return None



client = NVDApiClient(API_KEY)
data = client.get_vulnerabilities("Red Hat")
print(data)




"""
response = requests.get(URL)
if response.status_code == 200:
    logging.info("CVEs notificadas")
    print('Data:', response.json())
else:
    print('Error en la solicitud, detalles:', response.text)"""
