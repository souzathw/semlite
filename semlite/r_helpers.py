import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector

pandas2ri.activate()

def run_lavaan_sem(model_desc, csv_path, estimator="ML", ordered_vars=None):
    try:
        base = importr("base")
        utils = importr("utils")
        lavaan = importr("lavaan")

        robjects.r(f'df <- read.csv("{csv_path}")')
        robjects.r('df <- na.omit(df)')

        if ordered_vars:
            ordered_vector = StrVector(ordered_vars)
            robjects.r.assign("ordered_vars", ordered_vector)
            robjects.r('for (v in ordered_vars) { df[[v]] <- as.ordered(df[[v]]) }')
        robjects.r.assign("model", model_desc)

        robjects.r(f'fit <- sem(model, data = df, estimator = "{estimator}")')
        summary_result = robjects.r('capture.output(summary(fit, fit.measures = TRUE))')
        summary_list = list(summary_result)
        fit_indices = robjects.r('fitMeasures(fit)')
        indices = dict(zip(fit_indices.names, list(fit_indices)))
        est = robjects.r('parameterEstimates(fit, standardized = TRUE)')
        estimates_df = pandas2ri.rpy2py(est)

        return {
            "summary": summary_list,
            "indices": indices,
            "estimates": estimates_df
        }

    except Exception as e:
        raise RuntimeError(f"❌ Erro em run_lavaan_sem(): {e}")
