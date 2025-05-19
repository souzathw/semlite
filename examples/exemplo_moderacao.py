from semlite.moderation import run_moderation

result = run_moderation(
    data_path="data/teste_moderacao.csv",
    iv="DF",
    dv="FP",
    moderator="CR",
    interaction_type="product",
    indicators={
        "DF": ["DF1", "DF2", "DF3", "DF4"],
        "CR": ["JB2", "JB3", "JB4", "JB8", "JB13"],
        "FP": ["FP1", "FP2", "FP3", "FP4"]
    }
)

print("Modelo SEM com Moderação:")
print(result["model_description"])
print("\nEstimativas:")
print(result["estimates"])
print("\nEstatísticas de Ajuste:")
print(result["fit_stats"])