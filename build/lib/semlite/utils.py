import os
import pandas as pd
import csv

def validar_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Erro: O arquivo '{path}' não foi encontrado.")
    if not path.endswith('.csv'):
        raise ValueError(f"❌ Erro: O arquivo '{path}' não é um CSV válido.")

def validar_variaveis(df, variaveis):
    faltando = [var for var in variaveis if var not in df.columns]
    if faltando:
        raise ValueError(f"❌ Erro: As variáveis seguintes não estão no arquivo: {', '.join(faltando)}")

def print_sucesso(modelo="Modelo"):
    print(f"✅ {modelo} ajustado com sucesso.")
    print("📊 Resultados prontos para análise.")

def carregar_arquivo_robusto(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            sample = f.read(2048)
            dialect = csv.Sniffer().sniff(sample)
            f.seek(0)
            df = pd.read_csv(f, delimiter=dialect.delimiter)

        df.columns = df.columns.str.strip()
        df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

        return df

    except Exception as e:
        raise ValueError(f"❌ Erro ao carregar o arquivo CSV: {e}")
