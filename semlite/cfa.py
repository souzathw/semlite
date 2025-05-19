
from semopy import ModelMeans
import pandas as pd
from semlite.utils import validar_csv, validar_variaveis, print_sucesso

def run_cfa(data_path, factor_name, indicators):
    try:
        validar_csv(data_path)
        df = pd.read_csv(data_path, sep=';')
        validar_variaveis(df, indicators)

        model_desc = f"{factor_name} =~ " + " + ".join(indicators)

        model = ModelMeans(model_desc)
        model.fit(df)

        estimates = model.inspect(std_est=True)
        stats = model.calc_stats()

        print_sucesso("CFA")

        return {
            "model_description": model_desc,
            "estimates": estimates,
            "fit_stats": stats
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA: {e}")
        return None