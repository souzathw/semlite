from semopy import Model
from semlite.cfa import run_cfa

result = run_cfa(
    data_path="data/teste_cfa.csv",
    factor_name="DF",
    indicators=["DF1", "DF2", "DF3", "DF4"]
)

print("Modelo CFA:")
print(result["model_description"])
print("\nEstimativas:")
print(result["estimates"])
print("\nEstatísticas de Ajuste:")
print(result["fit_stats"])