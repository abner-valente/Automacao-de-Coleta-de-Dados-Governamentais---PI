import pandas as pd
import os

caminho = input("Digite o caminho da pasta onde estão os arquivos CSV: ")
arq_final = input("Digite o nome do arquivo final (ex: XX_unido.csv): ")
separador = input("Digite o separador dos arquivos CSV (padrão é ';'): ") or ';'

def consolidate_csv_files(directory_path, output_file, sep=separador):
    # Listar arquivos CSV no diretório
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    if not csv_files:
        print("Nenhum arquivo CSV encontrado no diretório.")
        return

    print(f"{len(csv_files)} arquivos CSV encontrados. Iniciando a consolidação...\n")

    frames = []

    for csv_file in csv_files:
        file_path = os.path.join(directory_path, csv_file)
        try:
            print(f"Lendo arquivo: {csv_file}")
            df = pd.read_csv(file_path, sep=sep)
            frames.append(df)
        except Exception as e:
            print(f"Erro ao ler o arquivo {csv_file}: {e}")

    # Concatenar os DataFrames se houver arquivos lidos com sucesso
    if frames:
        result = pd.concat(frames, ignore_index=True)
        result.to_csv(output_file, index=False, sep='|')
        print(f"\nConsolidação concluída! Arquivo salvo como: {output_file}")
    else:
        print("\nNenhum arquivo foi lido com sucesso. Nada foi salvo.")

# Parâmetros
directory_path = f"{caminho}/"
output_file = arq_final

consolidate_csv_files(directory_path, output_file)
