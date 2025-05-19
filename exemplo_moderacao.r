library(reticulate)
sem <- import_from_path("moderation", path = "caminho_da_pasta_semlite")

result <- sem$run_moderation(
  data_path = "caminho_do_csv",
  iv = "DF",
  dv = "FP",
  moderator = "CR",
  interaction_type = "product",  # ou "mean"
  indicators = dict(
    DF = c("DF1", "DF2", "DF3", "DF4"),
    CR = c("JB2", "JB3", "JB4", "JB8", "JB13"),
    FP = c("FP1", "FP2", "FP3", "FP4")
  )
)

cat(" Modelo SEM com moderação construído:\n")
cat(result$model_description, "\n\n")

cat(" Estimativas dos parâmetros:\n")
print(result$estimates)

cat("\n Métricas de Ajuste:\n")
print(result$fit_stats)
