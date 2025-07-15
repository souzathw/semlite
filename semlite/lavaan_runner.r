args <- commandArgs(trailingOnly = TRUE)

output_dir <- args[1]
estimator <- args[2]
ordered_vars <- if (length(args) >= 3) strsplit(args[3], ",")[[1]] else NULL

library(lavaan)

tryCatch({
  dados <- read.csv(file.path(output_dir, "dados.csv"))
  modelo <- paste(readLines(file.path(output_dir, "modelo.txt"), encoding = "UTF-8"), collapse = "\n")

  fit <- sem(
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

  if (!lavInspect(fit, "converged")) {
    stop("⚠️ O modelo não convergiu. Ajuste necessário.")
  }

  write.csv(parameterEstimates(fit, standardized = TRUE),
            file = file.path(output_dir, "estimates.csv"), row.names = FALSE)

  indices <- fitMeasures(fit, c("chisq", "df", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
  write.csv(data.frame(metric = names(indices), value = as.numeric(indices)),
            file = file.path(output_dir, "indices.csv"), row.names = FALSE)

  writeLines(capture.output(summary(fit, standardized = TRUE)),
             con = file.path(output_dir, "summary.txt"))

}, error = function(e) {
  msg <- paste("Erro em lavaan_runner.R:", conditionMessage(e))
  writeLines(msg, con = file.path(output_dir, "lavaan_error.log"))
  quit(save = "no", status = 1, runLast = FALSE)
})
