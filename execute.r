library(reticulate)
py_install("git+https://github.com/souzathw/semlite.git", pip = TRUE)
install.packages("lavaan")
sem <- import("semlite.moderation")

caminho_arquivo <- file.choose()
cat("Arquivo selecionado:", caminho_arquivo, "\n")

result <- sem$run_moderation(
  data_path = caminho_arquivo,
  iv = "SAUFAM",
  dv = "CULPA",
  moderator = "SSF",
  interaction_type = "product",
  indicators = dict(
    SAUFAM = c("SAUFAM1", "SAUFAM2", "SAUFAM3", "SAUFAM4", "SAUFAM5"),
    SSF = c("SSF1", "SSF2", "SSF3", "SSF4"),
    CULPA = c("CULPA1", "CULPA2", "CULPA3", "CULPA4", "CULPA5",
              "CULPA6", "CULPA7", "CULPA8", "CULPA9", "CULPA10")
  )
)

cat(" Modelo de Moderação construído:\n")
cat(result$model_description, "\n\n")

cat("Índices de ajuste:\n")
cat("CFI: ", result$fit_indices$cfi, "\n")
cat("TLI: ", result$fit_indices$tli, "\n")
cat("RMSEA: ", result$fit_indices$rmsea, "\n")
cat("SRMR: ", result$fit_indices$srmr, "\n")

cat("\n📊 Estimativas dos parâmetros (somente regressões):\n")
regs <- Filter(function(x) x$op == "~", result$estimates)
print(regs)

cat("\n Resumo do Lavaan:\n")
cat(result$summary, sep = "\n")
