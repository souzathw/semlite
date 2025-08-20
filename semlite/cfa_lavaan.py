import os
import pandas as pd
from semlite.utils import carregar_arquivo_robusto, validar_csv, validar_variaveis, print_sucesso
from rpy2 import robjects as r
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Ativa conversão automática de pandas <-> R
pandas2ri.activate()

# Importa pacotes R necessários
lavaan = importr("lavaan")
base = importr("base")

def montar_modelo(indicators: dict) -> str:
    """Monta a descrição do modelo Lavaan com múltiplos fatores."""
    linhas = []
    for fator, itens in indicators.items():
        linha = f"{fator} =~ " + " + ".join(itens)
        linhas.append(linha)
    return "\n".join(linhas)

def run_cfa(data_path, indicators, estimator="WLSMV"):
    try:
        validar_csv(data_path)
        df = carregar_arquivo_robusto(data_path)
        validar_variaveis(df, indicators)

        model_description = montar_modelo(indicators)
        r_df = pandas2ri.py2rpy(df)

        fit = lavaan.cfa(model_description, data=r_df, estimator=estimator)

        fit_indices = r["tryCatch"](
            r["fitMeasures"](fit, r.c("cfi", "tli", "rmsea", "srmr")),
            error=r("function(e) NULL")
        )

        estimates = base.summary(fit).rx2("PE")  

        print_sucesso("CFA (Lavaan)")
        return {
            "model_description": model_description,
            "fit_indices": dict(zip(["CFI", "TLI", "RMSEA", "SRMR"], list(fit_indices))) if fit_indices is not None else None,
            "estimates": estimates
        }

    except Exception as e:
        print(f"❌ Erro ao rodar a CFA (Lavaan): {e}")
        return None
