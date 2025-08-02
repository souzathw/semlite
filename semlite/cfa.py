from semlite.utils import validar_csv, carregar_arquivo_robusto, validar_variaveis, print_sucesso
from semlite.r_helpers import run_lavaan_cfa

def run_cfa(data_path, indicators, estimator="WLSMV", ordered_vars=None):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)

        todas_variaveis = [var for lista in indicators.values() for var in lista]
        validar_variaveis(df, todas_variaveis)

        result = run_lavaan_cfa(indicators, df, estimator, ordered_vars)
        print_sucesso("CFA")
        return result

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA: {e}")
        return None
