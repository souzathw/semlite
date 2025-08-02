args <- commandArgs(trailingOnly = TRUE)

output_dir <- args[1]
estimator <- args[2]
ordered_vars <- if (length(args) >= 3) strsplit(args[3], ",")[[1]] else NULL

library(lavaan)

dados <- read.csv(file.path(output_dir, "dados.csv"))
modelo <- paste(readLines(file.path(output_dir, "modelo.txt"), encoding = "UTF-8"), collapse = "\n")

fit <- tryCatch({
  sem(
    model = modelo,
    data = dados,
    estimator = estimator,
    fixed.x = FALSE,
    std.lv = TRUE,
    check.gradient = FALSE,
    start = "simple",
    ordered = ordered_vars,
    control = list(rel.tol = 1e-5, max.iter = 10000)
  )
}, error = function(e) {
  writeLines(c("ERRO ao ajustar o modelo:", e$message), file.path(output_dir, "error.txt"))
  stop(e)
})

write.csv(
  parameterEstimates(fit, standardized = TRUE),
  file = file.path(output_dir, "estimates.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

fit_indices <- tryCatch({
  fitMeasures(fit, c("chisq", "df", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
}, error = function(e) {
  writeLines(c("ERRO ao gerar indices:", e$message), file.path(output_dir, "indices_error.txt"))
  return(NULL)
})

if (!is.null(fit_indices)) {
  write.csv(
    data.frame(metric = names(fit_indices), value = unname(fit_indices)),
    file = file.path(output_dir, "indices.csv"),
    row.names = FALSE,
    fileEncoding = "UTF-8"
  )
}

writeLines(
  capture.output(summary(fit, standardized = TRUE, fit.measures = TRUE)),
  con = file.path(output_dir, "summary.txt")
)
