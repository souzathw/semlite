from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_arquivo_robusto
from semlite.r_helpers import run_lavaan_sem

def run_moderation(data_path, iv, dv, moderator, interaction_type='mean', indicators=None, estimator="WLSMV"):
    try:
        validar_csv(data_path)

        expected_columns = sum(indicators.values(), []) 
        df, _ = carregar_arquivo_robusto(
            data_path,
            colunas_esperadas=expected_columns,
            exportar_csv_limpo=False  
        )
        interaction_vars = []
        model_desc = ""

        for factor, items in indicators.items():
            model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

        if interaction_type == 'mean':
            df['IV_mean'] = df[indicators[iv]].mean(axis=1)
            df['MOD_mean'] = df[indicators[moderator]].mean(axis=1)
            df['interaction'] = df['IV_mean'] * df['MOD_mean']
            model_desc += f"{dv} ~ {iv} + {moderator} + interaction\n"

        elif interaction_type == 'product':
            for x in indicators[iv]:
                for z in indicators[moderator]:
                    col_name = f"{x}_{z}"
                    df[col_name] = df[x] * df[z]
                    interaction_vars.append(col_name)

            interaction_factor = f"{iv}_x_{moderator}"
            model_desc += f"{interaction_factor} =~ " + " + ".join(interaction_vars) + "\n"
            model_desc += f"{dv} ~ {iv} + {moderator} + {interaction_factor}\n"

        else:
            raise ValueError("❌ O parâmetro 'interaction_type' deve ser 'mean' ou 'product'.")
        temp_csv_path = "temp_clean.csv"
        df.to_csv(temp_csv_path, index=False)

        ordered_vars = indicators.get(dv, None)

        lavaan_result = run_lavaan_sem(
            model_desc=model_desc,
            csv_path=temp_csv_path,
            estimator=estimator,
            ordered_vars=ordered_vars
        )

        print(f"🧼 CSV limpo utilizado: {temp_csv_path}")
        print_sucesso("Moderação (via lavaan)")

        return {
            "model_description": model_desc,
            "fit_indices": lavaan_result["indices"],
            "estimates": lavaan_result["estimates"].to_dict(orient='records'),
            "summary": "\n".join(lavaan_result["summary"])
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a moderação: {e}")
        return None
