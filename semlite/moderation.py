from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_csv_robusto
from semlite.r_helpers import run_lavaan_sem

def run_moderation(data_path, iv, dv, moderator, interaction_type='mean', indicators=None, estimator="WLSMV"):
    try:
        validar_csv(data_path)
        df = carregar_csv_robusto(data_path)
        for itens in indicators.values():
            validar_variaveis(df, itens)

        model_desc = ""
        for factor, items in indicators.items():
            model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

        if interaction_type == 'mean':
            df['IV_mean'] = df[indicators[iv]].mean(axis=1)
            df['MOD_mean'] = df[indicators[moderator]].mean(axis=1)
            df['interaction'] = df['IV_mean'] * df['MOD_mean']

            model_desc += f"{dv} ~ {iv} + {moderator} + interaction\n"

        elif interaction_type == 'product':
            interaction_vars = []
            for x in indicators[iv]:
                for z in indicators[moderator]:
                    col_name = f"{x}_{z}"
                    df[col_name] = df[x] * df[z]
                    interaction_vars.append(col_name)

            interaction_factor = f"{iv}_x_{moderator}"

            model_desc += f"{interaction_factor} =~ " + " + ".join(interaction_vars) + "\n"
            model_desc += f"{dv} ~ {iv} + {moderator} + {interaction_factor}"

        else:
            raise ValueError("❌ O parâmetro 'interaction_type' deve ser 'mean' ou 'product'.")

        indices, estimates_df = run_lavaan_sem(model_desc, df, estimator=estimator)

        print_sucesso("Moderação (via lavaan)")

        return {
            "model_description": model_desc,
            "fit_indices": indices,
            "estimates": estimates_df.to_dict(orient='records')
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a moderação: {e}")
        return None
