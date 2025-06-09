library(reticulate)
py_install("git+https://github.com/souzathw/semlite.git")
sem <- import("semlite.moderation")


caminho_csv <- file.choose()
df <- read.csv(caminho_csv, sep = ",")  
print(colnames(df))

result <- sem$run_moderation(
  data_path = caminho_csv,
  iv = "SAUFAM",
  dv = "CULPA",
  moderator = "SSF",
  interaction_type = "product",  #ou "mean"
  indicators = dict(
    SAUFAM = c("SAUFAM1", "SAUFAM2", "SAUFAM3", "SAUFAM4", "SAUFAM5"),
    SSF = c("SSF1", "SSF2", "SSF3", "SSF4"),
    CULPA = c("CULPA1", "CULPA2", "CULPA3", "CULPA4", "CULPA5",
              "CULPA6", "CULPA7", "CULPA8", "CULPA9", "CULPA10")
  )
)

cat("📌 Modelo de Moderação construído:\n")
cat(result$model_description, "\n\n")

cat("📊 Estimativas dos parâmetros:\n")
print(result$estimates)