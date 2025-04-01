import json
import pandas as pd
from APISession import APISession

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

api = APISession(url)

dataframes = []
# Loop para obter dados da API

for i in range(1, 3500):
    try:
        response = api.get(f'{endpoint}?page={i}')
        
        if response.status_code == 404:
            print(f"Não há mais dados na página {i}.")
            break
        
        if response is None:
            print("Erro ao obter dados da API ou retorno vazio pelo fim dos dos dados.")
            break
        
        data = json.loads(response.text)
        if not data:
            print("Nenhum dado encontrado.")
            break
        
        df = pd.json_normalize(data['results'])
        dataframes.append(df)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")

    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    if dataframes:
        # Salvar em um arquivo CSV
        final_df = pd.concat(dataframes, ignore_index=True)
        print(f"Total de registros obtidos: {len(final_df)}")
    else:
        print("Nenhum dado encontrado.")

api.close()

#Salvar o DataFrame em um arquivo CSV
final_df.to_csv(f'PE_{ano_in}{mes_in}.csv', index=False, encoding='utf-8-sig')

