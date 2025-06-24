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

def carregar_arquivo_robusto(path):
    try:
        if path.endswith('.csv'):
            # Tentativa de detectar encoding com fallback
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

        # Limpar colunas e dados
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # Forçar conversão numérica e avisar se falhar
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception as e:
                print(f"⚠️ Aviso: Coluna '{col}' não pôde ser convertida para numérico.")

        # Remover linhas completamente vazias ou que ficaram com todos NaN
        df.dropna(how='all', inplace=True)

        return df

    except Exception as e:
        raise ValueError(f"❌ Erro ao carregar o arquivo: {e}")
