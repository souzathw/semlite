library(reticulate)
sem <- import_from_path("cfa", path = "caminho_da_pasta_semlite")

result <- sem$run_cfa(
  data_path = "caminho_do_csv",
  factor_name = "DF",
  indicators = c("DF1", "DF2", "DF3", "DF4")
)

cat(" Modelo CFA construído:\n")
cat(result$model_description, "\n\n")

cat(" Estimativas dos parâmetros:\n")
print(result$estimates)

cat("\n Métricas de Ajuste:\n")
print(result$fit_stats)



