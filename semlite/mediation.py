from semopy import ModelMeans
from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_arquivo_robusto

def run_mediation(data_path, iv, mediator, dv, indicators):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)
        for itens in indicators.values():
            validar_variaveis(df, itens)

        model_desc = ""
        for factor, items in indicators.items():
            model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

        model_desc += f"{mediator} ~ {iv}\n{dv} ~ {mediator} + {iv}"

        model = ModelMeans(model_desc)
        model.fit(df)

        estimates = model.inspect(std_est=True)
        print_sucesso("Mediação")

        return {
            "model_description": model_desc,
            "estimates": estimates
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a mediação: {e}")
        return None
