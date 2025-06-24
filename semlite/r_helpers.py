import rpy2.robjects as ro
from rpy2.robjects.vectors import StrVector

def run_lavaan_sem(model_desc, df=None, csv_path="temp_clean.csv", estimator="WLSMV", ordered_vars=None):
    ro.r('library(lavaan)')
    ro.r.assign("modelo", model_desc)
    if not csv_path or not csv_path.endswith(".csv"):
        raise ValueError("❌ Caminho para CSV limpo inválido ou ausente.")

    ro.r.assign("caminho_csv", csv_path)
    ro.r('dados1 <- read.csv(caminho_csv, stringsAsFactors = FALSE)')
    ro.r('dados1 <- na.omit(dados1)')

    if ordered_vars is not None:
        ro.globalenv['ordered_vars'] = StrVector(ordered_vars)
        ro.r(f'''
        fit <- sem(model=modelo, data=dados1, ordered=ordered_vars, estimator="{estimator}")
        ''')
    else:
        ro.r(f'''
        fit <- sem(model=modelo, data=dados1, estimator="{estimator}")
        ''')

    converged = bool(ro.r('lavInspect(fit, "converged")')[0])
    if not converged:
        raise RuntimeError("❌ lavaan->lav_fit_measures(): fit measures not available if model did not converge")

    ro.r('''
    indices <- fitMeasures(fit, c("chisq", "df", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
    estimates <- parameterEstimates(fit, standardized=TRUE)
    resumo <- capture.output(summary(fit, standardized=TRUE))
    ''')

    indices = dict(zip(ro.r('names(indices)'), list(ro.r('indices'))))
    estimates_df = ro.conversion.rpy2py(ro.r('estimates'))
    resumo_list = list(ro.r('resumo'))

    return {
        "indices": indices,
        "estimates": estimates_df,
        "summary": resumo_list
    }
