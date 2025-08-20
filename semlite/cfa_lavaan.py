from semlite.utils import validar_csv, validar_variaveis, carregar_arquivo_robusto, print_sucesso
from semlite.r_helpers import run_lavaan_cfa

def run_cfa(data_path, indicators, estimator="WLSMV", ordered_vars=None):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)
        for lista in indicators.values():
            validar_variaveis(df, lista)
        result = run_lavaan_cfa(factor_models=indicators, df=df, estimator=estimator, ordered_vars=ordered_vars)
        print_sucesso("CFA")
        print("📊 Resultados prontos para análise.")

        return {
            "model_description": "\n".join([f"{k} =~ {' + '.join(v)}" for k, v in indicators.items()]),
            "estimates": result["estimates"],
            "fit_indices": result["indices"],
            "summary": result["summary"]
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA: {e}")
        return None
