library(reticulate)
sem <- import_from_path("mediation", path = "caminho_da_pasta_semlite")

result <- sem$run_mediation(
  data_path = "caminho_do_csv",
  iv = "DF",
  mediator = "AA",
  dv = "FP",
  indicators = dict(
    DF = c("DF1", "DF2", "DF3", "DF4"),
    AA = c("AA1", "AA2REC", "AA3", "AA4REC"),
    FP = c("FP1", "FP2", "FP3", "FP4")
  )
)

cat(" Modelo SEM construído:\n")
cat(result$model_description, "\n\n")

cat(" Estimativas dos parâmetros:\n")
print(result$estimates)

cat("\n Métricas de Ajuste:\n")
print(result$fit_stats)
