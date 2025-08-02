import json
import pandas as pd
import logging
import asyncio
from APISession import APISession

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

url = 'https://transparencia2.pi.gov.br/api/v1/'

# Entrada do usuário
while True:
    ano_in = input("Digite o ano da consulta (ex: 2024): ").strip()
    if ano_in.isdigit() and 2000 <= int(ano_in) <= 2100:
        break

while True:
    mes_in = input("Digite o mês da consulta (ex: 01 para Janeiro): ").strip()
    if mes_in.isdigit() and 1 <= int(mes_in) <= 12:
        mes_in = mes_in.zfill(2)
        break

endpoint = f"servidores/{ano_in}/{mes_in}/"
MAX_PAGES = 3500
CONCURRENCY = 10  # Quantas requisições simultâneas

async def fetch_page(api, endpoint, page, semaphore):
    url = f"{endpoint}?page={page}"
    async with semaphore:
        try:
            response = await api.get(url)
            if response is None:
                logging.error(f"Erro ao obter dados da API na página {page}. RESPONSE is None.")
                return None
            if response.status_code == 404:
                # Nenhum dado a partir desta página
                return "404"

            print(f"Obtendo dados da página {page}...")
            
            data = json.loads(response.text)
            if not data or 'results' not in data or not data['results']:
                return None
            df = pd.json_normalize(data['results'])
            return df
        except Exception as e:
            logging.error(f"Erro ao processar página {page}: {e}")
            return None

async def main():
    api = APISession(url)
    semaphore = asyncio.Semaphore(CONCURRENCY)
    dataframes = []
    tasks = []

    # Cria tarefas para todas as páginas
    for i in range(1, MAX_PAGES+1):
        tasks.append(fetch_page(api, endpoint, i, semaphore))

    # Executa em paralelo (espera todas terminarem)
    responses = await asyncio.gather(*tasks)

    # Processa resultados
    for idx, res in enumerate(responses, 1):
        if isinstance(res, str) and res == "404":
            print(f"Parando na página {idx}: status 404.")
            break
            break
        if res is not None:
            dataframes.append(res)

    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)
        print(f"Total de registros obtidos: {len(final_df)}")
        final_df.to_csv(f'PE_{ano_in}{mes_in}.csv', index=False, encoding='utf-8-sig')
    else:
        print("Nenhum dado encontrado.")

    await api.close()

if __name__ == "__main__":
    asyncio.run(main())
