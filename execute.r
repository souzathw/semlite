library(reticulate)
use_python("/home/th/.cache/R/reticulate/uv/cache/archive-v0/2ZFEmkvCeQxZ308ijiMFV/bin/python3", required = TRUE)
sem <- import_from_path("moderation", path = "/home/th/Desktop/semlite/semlite")

result <- sem$run_moderation(
  data_path = "/home/th/Desktop/semlite/data/teste_moderacao.csv",
  iv = "DF",
  dv = "FP",
  moderator = "CR",
  interaction_type = "product", 
  indicators = dict(
    DF = c("DF1", "DF2", "DF3", "DF4"),
    CR = c("JB2", "JB3", "JB4", "JB8", "JB13"),
    FP = c("FP1", "FP2", "FP3", "FP4")
  )
)

cat("Modelo SEM com moderação construído:\n")
cat(result$model_description, "\n\n")

cat("Estimativas dos parâmetros:\n")
print(result$estimates)

cat("\n Métricas de Ajuste:\n")
print(result$fit_stats)
