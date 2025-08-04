# Automação dos Servidores Estaduais do Estado do PI

O Script tem como objetivo coletar os dados dos servidores estaduais do AP do Link: https://www.transparencia.pi.gov.br/pessoal/

A automação de coleta de dados dos servidores públicos estaduais pelo portal da transparência do Piauí faz uma ordenação nos arquivos, verificando se a estrutura está padronizada e unificando todas as informações em dataframes para por fim ser salva em um arquivo CSV.

## Venv

### Bibliotecas

- Pandas
- Asyncio
- Httpx

```bash
	pip install pandas==2.2.2 httpx==0.28.1 asyncio-3.4.3
```

### Python

- Python 3.12.5

## Execução

Após instalar as bibliotecas principais usadas basta abrir o Power Shell na pasta onde foi baixada os scripts e executar:

```bash
py getPEapi.py
```

Colocar os dados de input e executar.
