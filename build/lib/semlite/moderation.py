from semopy import ModelMeans
from semlite.utils import validar_csv, validar_variaveis, print_sucesso, carregar_csv_robusto

def run_moderation(data_path, iv, dv, moderator, interaction_type='mean', indicators=None):
    try:
        validar_csv(data_path)
        df = carregar_csv_robusto(data_path)
        for itens in indicators.values():
            validar_variaveis(df, itens)

        model_desc = ""
        for factor, items in indicators.items():
            model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

        if interaction_type == 'mean':
            df['interaction'] = df[indicators[iv]].mean(axis=1) * df[indicators[moderator]].mean(axis=1)
            model_desc += f"{dv} ~ {iv} + {moderator} + interaction"
        elif interaction_type == 'product':
            for x in indicators[iv]:
                for z in indicators[moderator]:
                    col_name = f"{x}_{z}"
                    df[col_name] = df[x] * df[z]
            interaction_vars = [f"{x}_{z}" for x in indicators[iv] for z in indicators[moderator]]
            model_desc += "Interaction =~ " + " + ".join(interaction_vars) + "\n"
            model_desc += f"{dv} ~ {iv} + {moderator} + Interaction"
        else:
            raise ValueError("❌ O parâmetro 'interaction_type' deve ser 'mean' ou 'product'.")

        model = ModelMeans(model_desc)
        model.fit(df)

        estimates = model.inspect(std_est=True)
        print_sucesso("Moderação")

        return {
            "model_description": model_desc,
            "estimates": estimates
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a moderação: {e}")
        return None
