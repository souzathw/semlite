import os
import pandas as pd
import csv

def validar_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Erro: O arquivo '{path}' não foi encontrado.")
    if not (path.endswith('.csv') or path.endswith('.xlsx')):
        raise ValueError(f"❌ Erro: O arquivo '{path}' não é CSV nem XLSX válido.")

def validar_variaveis(df, variaveis):
    faltando = [v for v in variaveis if v not in df.columns]
    if faltando:
        raise ValueError(f"❌ Erro: Faltam colunas: {', '.join(faltando)}")

def carregar_csv_robusto(path):
    if path.endswith('.csv'):
        for enc in ('utf-8', 'latin1', 'utf-16'):
            try:
                with open(path, encoding=enc) as f:
                    sample = f.read(2048); f.seek(0)
                    dialect = csv.Sniffer().sniff(sample)
                    df = pd.read_csv(f, delimiter=dialect.delimiter)
                break
            except Exception:
                continue
        else:
            df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    df = df.apply(lambda c: c.str.strip() if c.dtype == object else c)
    df = df.apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)
    return df
