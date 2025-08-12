# Projeto de Automação dos Servidores Estaduais do Estado do PI

## Objetivo

O projeto tem como objetivo coletar os dados dos servidores estaduais do PI do link: https://www.transparencia.pi.gov.br/pessoal/  salva-las em um banco de dados e realizar métricas com uma ferramenta de BI. Para esse projeto será feita requisição de todos as remunerações do ano de 2024.

A automação de coleta de dados dos servidores públicos estaduais pelo portal da transparência do Piauí faz uma ordenação nos arquivos, verificando se a estrutura está padronizada e unificando todas as informações em dataframes para por fim ser salva em um arquivo CSV. Depois de salvo, é feito uma importação para um banco Postgres, onde serve de base para serem realizadas as métricas no Power BI.

## Python

### venv

- Python 3.12.5

### Bibliotecas

- Pandas
- Asyncio
- Httpx

```bash
	pip install pandas==2.2.2 httpx==0.28.1 asyncio-3.4.3
```

## Banco de Dados

- Postgres 15 - alpine

Usado em ambiente Docker:

```powershell
docker run -d \
  --name postgres-container \
  --network host \
  -e POSTGRES_USER=****\
  -e POSTGRES_PASSWORD=*****\
  -e POSTGRES_DB=meu_db \
  -p 15432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15-alpine
```

Criação da tabela e indexes para receber os dados:

```sql
CREATE TABLE servidores_estaduais_pi (
    id                              int,
    ano                             TEXT,
    nome                            TEXT,
    matricula                       TEXT,
    categoria                       TEXT,
    orgao_nome                      TEXT,
    cargo_nome                      TEXT,
    data_exoneracao                 date,
    jornada_semanal_ch              TEXT,
    remuneracao_bruta               numeric,
    remuneracao_basica              numeric,
    remuneracao_variavel            numeric,
    remuneracao_eventual            numeric,
    deducoes_legais                 numeric,
    remuneracao_apos_deducoes_legais numeric
);

CREATE INDEX IDX_MAT_ID ON servidores_estaduais_pi(matricula, id);
```

## Execução

### 1. Requisição

Após instalar as bibliotecas principais usadas basta abrir o Power Shell na pasta onde foi baixada é rodado o scripts e executar:

```bash
py getPEapi.py
```

É requerido o ano e o mês da remuneração do servidores. Depois disso começa os downloads de requisição. 

Como dito antes, para esse projeto foi feita as requisições de todo o ano de 2024.

Após os downloads os arquivos foram unificados com o módulo `unir_arq.py` :

```bash
py unir_arq.py
```

É requirido a pasta dos arquivos .csv e o delimitador deles. O resultado é um arquivo só unificando todos os .csv com o delimitador *pipe* “|”.

### 2. Inserção no banco de dados

Abre-se a ide do Postgres (PgAdmin4 no meu caso) e após conectar no banco de dados abre-se uma query tool:

```sql
COPY servidores_estaduais_pi
FROM '/var/lib/postgresql/data/PI_2024_unido.csv'
WITH (FORMAT csv, HEADER true, DELIMITER '|');
```

> ⚠️ É importante garantir que o arquivo unificado estará no diretório que o Postgres tem permissão de acessar.
>
