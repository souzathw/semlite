from semopy import ModelMeans
from semopy.stats import calc_stats
from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_arquivo_robusto

def run_cfa(data_path, indicators):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)

        for lista in indicators.values():
            validar_variaveis(df, lista)

        partes = [f"{fator} =~ {' + '.join(itens)}" for fator, itens in indicators.items()]
        model_desc = "\n".join(partes)

        model = ModelMeans(model_desc)
        model.fit(df)
        estimates = model.inspect(std_est=True)
        stats = calc_stats(model)

        fit_indices = {
            "Chi-Square": stats["chi2"],
            "df": stats["DoF"],
            "CFI": stats["CFI"],
            "TLI": stats["TLI"],
            "RMSEA": stats["RMSEA"],
            "RMSEA_low": stats.get("RMSEA_low", None),
            "RMSEA_high": stats.get("RMSEA_high", None),
            "SRMR": stats["SRMR"]
        }

        print_sucesso("CFA")
        print("📊 Resultados prontos para análise.")

        return {
            "model_description": model_desc,
            "estimates": estimates,
            "fit_indices": fit_indices
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA: {e}")
        return None
