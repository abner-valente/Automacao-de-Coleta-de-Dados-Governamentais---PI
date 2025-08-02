import httpx
from typing import Optional
import logging

logging.basicConfig(filename='app_api.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class APISession:
    def __init__(self, base_url: str, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[tuple] = None):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            headers=headers,
            cookies=cookies,
            auth=auth,
            verify=False  # cuidado em produção!
        )

    async def get(self, endpoint: str, params: Optional[dict] = None, timeout: int = 60):
        url = self.base_url + endpoint
        try:
            response = await self.client.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            print(f"❌ Erro GET em {url}: {e}")
            logging.error(f"Erro GET em {url}: {e}")
            return None

    async def post(self, endpoint: str, data: Optional[dict] = None, json: Optional[dict] = None, timeout: int = 60):
        url = self.base_url + endpoint
        try:
            response = await self.client.post(url, data=data, json=json, timeout=timeout)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            print(f"❌ Erro POST em {url}: {e}")
            logging.error(f"Erro POST em {url}: {e}")
            return None

    async def close(self):
        await self.client.aclose()
