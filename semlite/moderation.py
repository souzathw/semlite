from semlite.utils import validar_csv, validar_variaveis, carregar_csv_robusto
from semlite.r_helpers import run_lavaan_sem

def run_moderation(data_path, iv, dv, moderator,
                   interaction_type='mean', indicators=None,
                   estimator="WLSMV"):
    try:

        validar_csv(data_path)
        df = carregar_csv_robusto(data_path)
        
        for items in indicators.values():
            validar_variaveis(df, items)

        model_desc = ""
        for factor, items in indicators.items():
            model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

        if interaction_type == 'mean':
            df['IV_mean'] = df[indicators[iv]].mean(axis=1)
            df['MOD_mean'] = df[indicators[moderator]].mean(axis=1)
            df['interaction'] = df['IV_mean'] * df['MOD_mean']
            model_desc += f"{dv} ~ {iv} + {moderator} + interaction\n"
        else:  
            inter_cols = []
            for x in indicators[iv]:
                for z in indicators[moderator]:
                    col = f"{x}_{z}"
                    df[col] = df[x] * df[z]
                    inter_cols.append(col)
            factor_name = f"{iv}_x_{moderator}"
            model_desc += f"{factor_name} =~ " + " + ".join(inter_cols) + "\n"
            model_desc += f"{dv} ~ {iv} + {moderator} + {factor_name}\n"

        csv_clean = "temp_clean.csv"
        df.to_csv(csv_clean, index=False)

        ordered = indicators.get(dv)
        res = run_lavaan_sem(model_desc, csv_clean, estimator=estimator, ordered_vars=ordered)
        estimates = res["estimates"]
        estimates = estimates.to_dict(orient="records")

        return {
            "model_description": model_desc,
            "fit_indices": res["indices"],
            "estimates": estimates,
            "summary": "\n".join(res["summary"])
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a moderação: {e}")
        return None
