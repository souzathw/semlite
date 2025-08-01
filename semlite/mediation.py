from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_arquivo_robusto
from semlite.r_helpers import run_lavaan_sem

def run_mediation(data_path, iv, mediator, dv, indicators):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)
        for itens in indicators.values():
            validar_variaveis(df, itens)

        model_desc = ""
        for factor, items in indicators.items():
            model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

        model_desc += f"{mediator} ~ {iv}\n"
        model_desc += f"{dv} ~ {mediator} + {iv}"
        result = run_lavaan_sem(model_desc, df)

        print_sucesso("Mediação")

        return {
            "model_description": model_desc,
            "fit_indices": result["indices"],
            "estimates": result["estimates"],
            "summary": result["summary"]
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a mediação: {e}")
        return None
