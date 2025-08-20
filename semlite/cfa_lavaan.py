from semlite.r_helpers import run_lavaan_cfa
from semlite.utils import validar_csv, validar_variaveis, carregar_arquivo_robusto, print_sucesso

def run_cfa(data_path, indicators, estimator="WLSMV", ordered_vars=None):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)

        for lista in indicators.values():
            validar_variaveis(df, lista)
        result = run_lavaan_cfa(indicators, df, estimator=estimator, ordered_vars=ordered_vars)

        print_sucesso("CFA (via lavaan)")
        print("📊 Resultados prontos para análise.")

        return {
            "model_description": "\n".join(
                [f"{fator} =~ {' + '.join(itens)}" for fator, itens in indicators.items()]
            ),
            "estimates": result["estimates"],
            "fit_indices": result["indices"],
            "summary": result["summary"]
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA (lavaan): {e}")
        return None
