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
                    samp = f.read(2048); f.seek(0)
                    delim = csv.Sniffer().sniff(samp).delimiter
                    df = pd.read_csv(f, delimiter=delim)
                break
            except Exception:
                continue
        else:
            df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    # strip em strings
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()
    # força numérico
    df = df.apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)
    return df
