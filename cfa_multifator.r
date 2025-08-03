library(reticulate)
pip <- gsub("python.exe", "pip.exe", py_config()$python)
system2(pip, c("uninstall", "-y", "semlite"))

py_install("git+https://github.com/souzathw/semlite.git", pip = TRUE)
py_install("chardet", pip = TRUE)
install.packages("lavaan")
sem <- import("semlite.cfa")

caminho_arquivo <- file.choose()
cat(" Arquivo selecionado:", caminho_arquivo, "\n")

indicators <- dict(
  SAUFAM = c("SAUFAM1", "SAUFAM2", "SAUFAM3", "SAUFAM4", "SAUFAM5"),
  SSF = c("SSF1", "SSF2", "SSF3", "SSF4"),
  CULPA = c("CULPA1", "CULPA2", "CULPA3", "CULPA4", "CULPA5",
            "CULPA6", "CULPA7", "CULPA8", "CULPA9", "CULPA10")
)

result <- sem$run_cfa(
  data_path = caminho_arquivo,
  indicators = indicators
)

cat("\n Modelo de CFA construído:\n")
cat(result$model_description, "\n\n")
if (!is.null(result$fit_indices)) {
  cat("CFI: ", result$fit_indices[["CFI"]], "\n")
  cat("TLI: ", result$fit_indices[["TLI"]], "\n")
  cat("RMSEA: ", result$fit_indices[["RMSEA"]], "\n")
  cat("SRMR: ", result$fit_indices[["SRMR"]], "\n")
} else {
  cat(" Índices de ajuste não disponíveis.\n")
}

cat("\n Estimativas dos parâmetros:\n")
print(result$estimates)
