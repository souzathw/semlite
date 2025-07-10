import os
import pandas as pd
import csv
import chardet

def validar_csv(path):
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ Erro: O arquivo '{path}' não foi encontrado.")
    if not path.lower().endswith('.csv'):
        raise ValueError(f"❌ Erro: O arquivo '{path}' não possui extensão CSV válida.")

def validar_variaveis(df, colunas):
     
    faltando = [col for col in colunas if col not in df.columns]
    if faltando:
        raise ValueError(f"❌ Erro: As seguintes colunas estão ausentes no arquivo: {', '.join(faltando)}")

def print_sucesso(modelo="Modelo"):
    
    print(f"✅ {modelo} ajustado com sucesso.")
    print("📊 Resultados prontos para análise.")

def detectar_encoding(path):
    with open(path, 'rb') as f:
        result = chardet.detect(f.read(4096))
    return result['encoding']

def carregar_arquivo_robusto(path, encoding=None, delimitadores=[',', ';', '\t', '|']):
    if encoding is None:
        encoding = detectar_encoding(path)
    
    with open(path, 'r', encoding=encoding) as f:
        amostra = f.read(2048)
        try:
            dialecto = csv.Sniffer().sniff(amostra, delimiters=''.join(delimitadores))
            delimitador = dialecto.delimiter
        except csv.Error:
            delimitador = max(delimitadores, key=lambda d: amostra.count(d))
    
    df = pd.read_csv(
        path,
        encoding=encoding,
        delimiter=delimitador,
        skip_blank_lines=True,
        comment='#'
    )
    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.str.strip() if col.dtypes == 'object' else col)
    return df
