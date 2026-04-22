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
        self.base_url = "https://services.nvd.nist.gov/rest/json/cpes/2.0?keywordSearch="
        self.headers = {"apiKey": api_key}
        # Con API Key, el límite es ~50 peticiones cada 30 segundos.
        # Un delay de 0.6s entre llamadas es seguro.
        self.delay = 0.6

    def get_vulnerabilities(self, cpe_name):
        params = {"keywordSearch": cpe_name.replace(" ", "%20"),
                    "resultsPerPage": 5}
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
                logging.error("Posible baneo temporal o API Key invalida.")
            else:
                logging.error(f"Error al obtener vulnerabilidades: {response.status_code}-{response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error al obtener vulnerabilidades: {e}")

        time.sleep(self.delay)
        return None



client = NVDApiClient(API_KEY)
data = client.get_vulnerabilities("Red Hat Microsoft Debian")
print(data)
