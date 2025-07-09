import os
import pandas as pd
import csv
import chardet

def verificar_arquivo_csv(caminho):
    """Valida se o arquivo existe e se tem extensão .csv"""
    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"❌ Erro: O arquivo '{caminho}' não foi encontrado.")
    if not caminho.lower().endswith('.csv'):
        raise ValueError(f"❌ Erro: O arquivo '{caminho}' não possui extensão CSV válida.")

def verificar_colunas_existentes(df, colunas_esperadas):
    """Verifica se todas as colunas esperadas estão presentes no DataFrame"""
    colunas_faltando = [col for col in colunas_esperadas if col not in df.columns]
    if colunas_faltando:
        raise ValueError(f"❌ Erro: As seguintes colunas estão ausentes no arquivo: {', '.join(colunas_faltando)}")

def exibir_sucesso(nome_modelo="Modelo"):
    """Exibe mensagem de sucesso do ajuste"""
    print(f"✅ {nome_modelo} ajustado com sucesso.")
    print("📊 Resultados prontos para análise.")

def detectar_encoding(caminho):
    with open(caminho, 'rb') as f:
        resultado = chardet.detect(f.read(4096))
    return resultado['encoding']

def carregar_csv_robusto(caminho, encoding=None, delimitadores=[',', ';', '\t', '|']):
    # Detecta encoding se não fornecido
    if encoding is None:
        encoding = detectar_encoding(caminho)
    
    # Tenta detectar delimitador
    with open(caminho, 'r', encoding=encoding) as arquivo:
        amostra = arquivo.read(2048)
        try:
            dialecto = csv.Sniffer().sniff(amostra, delimiters=''.join(delimitadores))
            delimitador = dialecto.delimiter
        except csv.Error:
            # Tenta encontrar delimitador mais comum manualmente
            delimitador = max(delimitadores, key=lambda d: amostra.count(d))
    
    # Lê o arquivo
    df = pd.read_csv(
        caminho,
        encoding=encoding,
        delimiter=delimitador,
        skip_blank_lines=True,
        comment='#'
    )
    # Limpa espaços em branco
    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.str.strip() if col.dtypes == 'object' else col)
    return df