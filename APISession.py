import requests
from typing import Optional
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class APISession:
    def __init__(self, base_url: str, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[tuple] = None):
        self.session = requests.Session()
        self.base_url = base_url

        # Configura headers padrão (se houver)
        if headers:
            self.session.headers.update(headers)
        
        # Configura cookies padrão (se houver)
        if cookies:
            self.session.cookies.update(cookies)

        # Configura autenticação básica (opcional)
        if auth:
            self.session.auth = auth

    def get(self, endpoint: str, params: Optional[dict] = None, timeout: int = 60):
        url = self.base_url + endpoint
        try:
            response = self.session.get(url, params=params, timeout=timeout, verify=False)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"❌ Erro GET em {url}: {e}")
            return None

    def post(self, endpoint: str, data: Optional[dict] = None, json: Optional[dict] = None, timeout: int = 60):
        url = self.base_url + endpoint
        try:
            response = self.session.post(url, data=data, json=json, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"❌ Erro POST em {url}: {e}")
            return None

    def close(self):
        self.session.close()