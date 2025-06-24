import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

pandas2ri.activate()
lavaan = importr("lavaan")

def run_lavaan_sem(model_desc: str, csv_path: str, estimator: str = "WLSMV", ordered_vars=None):
    ro.r(f'df <- read.csv("{csv_path}", stringsAsFactors=FALSE)')
    ro.r('df <- na.omit(df)')
    if ordered_vars:
        ro.globalenv['ordered_vars'] = ro.StrVector(ordered_vars)
        ro.r('for(v in ordered_vars) df[[v]] <- as.ordered(df[[v]])')
    ro.globalenv['model_desc'] = model_desc
    ro.r(f'fit <- sem(model_desc, data=df, estimator="{estimator}")')
    ro.r('indices <- fitMeasures(fit)')
    ro.r('estimates <- parameterEstimates(fit, standardized=TRUE)')
    ro.r('summary_txt <- capture.output(summary(fit, fit.measures=TRUE, standardized=TRUE))')
    indices = dict(zip(ro.r('names(indices)'), list(ro.r('indices'))))
    estimates_df = pandas2ri.rpy2py(ro.r('estimates'))
    summary_list = list(ro.r('summary_txt'))
    return {"indices": indices, "estimates": estimates_df, "summary": summary_list}
