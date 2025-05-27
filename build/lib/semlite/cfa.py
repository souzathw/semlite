from semopy import ModelMeans
from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_csv_robusto

def run_cfa(data_path, factor_name, indicators):
    try:
        validar_csv(data_path)
        df = carregar_csv_robusto(data_path)
        validar_variaveis(df, indicators)

        model_desc = f"{factor_name} =~ " + " + ".join(indicators)

        model = ModelMeans(model_desc)
        model.fit(df)

        estimates = model.inspect(std_est=True)
        print_sucesso("CFA")

        return {
            "model_description": model_desc,
            "estimates": estimates
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA: {e}")
        return None
