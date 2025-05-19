
from semopy import Model
import pandas as pd

def run_moderation(data_path, iv, dv, moderator, interaction_type='mean', indicators=None):
    df = pd.read_csv(data_path, sep=';')

    model_desc = ""
    for factor, items in indicators.items():
        model_desc += f"{factor} =~ " + " + ".join(items) + "\n"

    if interaction_type == 'mean':
        df['interaction'] = df[indicators[iv]].mean(axis=1) * df[indicators[moderator]].mean(axis=1)
    elif interaction_type == 'product':
        for i, x in enumerate(indicators[iv]):
            for j, z in enumerate(indicators[moderator]):
                col_name = f"{x}_{z}"
                df[col_name] = df[x] * df[z]
        interaction_vars = [f"{x}_{z}" for x in indicators[iv] for z in indicators[moderator]]
        model_desc += "Interaction =~ " + " + ".join(interaction_vars) + "\n"
    else:
        raise ValueError("interaction_type deve ser 'mean' ou 'product'.")

    if interaction_type == 'mean':
        model_desc += f"{dv} ~ {iv} + {moderator} + interaction"
    else:
        model_desc += f"{dv} ~ {iv} + {moderator} + Interaction"

    model = Model(model_desc)
    model.fit(df)

    estimates = model.inspect(std_est=True)
    stats = model.inspect()


    return {
        "model_description": model_desc,
        "estimates": estimates,
        "fit_stats": stats
    }