from semlite.utils import carregar_arquivo_robusto, validar_csv, validar_variaveis
from semlite.r_helpers import run_lavaan_cfa

def run_cfa(data_path, indicators, estimator="WLSMV", ordered_vars=None):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)

        for lista in indicators.values():
            validar_variaveis(df, lista)

        result = run_lavaan_cfa(indicators, df, estimator=estimator, ordered_vars=ordered_vars)

        print("✅ CFA (Lavaan) ajustada com sucesso.")
        print("📊 Resultados prontos para análise.")

        return {
            "model_description": "\n".join([f"{k} =~ {' + '.join(v)}" for k, v in indicators.items()]),
            "estimates": result["estimates"],
            "fit_indices": result["indices"],
            "summary": result["summary"]
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA (Lavaan): {e}")
        return None
