import os
import pandas as pd
import csv

def validar_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Erro: O arquivo '{path}' não foi encontrado.")
    if not (path.endswith('.csv') or path.endswith('.xlsx')):
        raise ValueError(f"❌ Erro: O arquivo '{path}' não é CSV nem XLSX válido.")

def validar_variaveis(df, variaveis):
    faltando = [var for var in variaveis if var not in df.columns]
    if faltando:
        raise ValueError(f"❌ Erro: As variáveis seguintes não estão no arquivo: {', '.join(faltando)}")

def print_sucesso(modelo="Modelo"):
    print(f"✅ {modelo} ajustado com sucesso.")
    print("📊 Resultados prontos para análise.")

def carregar_arquivo_robusto(path, colunas_esperadas=None, exportar_csv_limpo=True):
    try:
        if path.endswith('.csv'):
            encodings = ['utf-8', 'latin1', 'utf-16']
            for enc in encodings:
                try:
                    with open(path, 'r', encoding=enc) as f:
                        sample = f.read(2048)
                        f.seek(0)
                        try:
                            dialect = csv.Sniffer().sniff(sample)
                            df = pd.read_csv(f, delimiter=dialect.delimiter)
                        except csv.Error:
                            f.seek(0)
                            df = pd.read_csv(f, sep=None, engine='python')
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("❌ Erro: Não foi possível detectar o encoding do arquivo CSV.")
        elif path.endswith('.xlsx'):
            df = pd.read_excel(path)
        else:
            raise ValueError("❌ Formato de arquivo não suportado. Use .csv ou .xlsx.")


        df.columns = df.columns.str.strip()
        df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))


        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)

        if colunas_esperadas:
            validar_variaveis(df, colunas_esperadas)


        if exportar_csv_limpo:
            temp_path = "temp_clean.csv"
            df.to_csv(temp_path, index=False)
            return df, temp_path
        else:
            return df, None   

    except Exception as e:
        raise ValueError(f"❌ Erro ao carregar o arquivo: {e}")
