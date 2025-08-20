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

        try:
            model.fit(df)
        except Exception as e:
            print(f"❌ Falha no ajuste do modelo: {e}")
            return {
                "model_description": model_desc,
                "estimates": None,
                "fit_indices": None
            }

        try:
            estimates = model.inspect(std_est=True)
        except Exception:
            estimates = None

        try:
            stats = calc_stats(model)
            fit_indices = {
                "Chi-Square": stats.get("chi2"),
                "df": stats.get("DoF"),
                "CFI": stats.get("CFI"),
                "TLI": stats.get("TLI"),
                "RMSEA": stats.get("RMSEA"),
                "RMSEA_low": stats.get("RMSEA_low"),
                "RMSEA_high": stats.get("RMSEA_high"),
                "SRMR": stats.get("SRMR")
            }
        except Exception:
            fit_indices = None

        print_sucesso("CFA")
        print("📊 Resultados prontos para análise.")

        return {
            "model_description": model_desc,
            "estimates": estimates,
            "fit_indices": fit_indices
        }

    except Exception as e:
        print(f"❌ Erro geral ao rodar a CFA: {e}")
        return None
