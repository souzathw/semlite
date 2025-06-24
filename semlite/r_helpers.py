import rpy2.robjects as ro
from rpy2.robjects.vectors import StrVector
from pathlib import Path

def run_lavaan_sem(model_desc, csv_path="temp_clean.csv", estimator="WLSMV", ordered_vars=None):
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"❌ Arquivo CSV não encontrado: {csv_path}")

    ro.r('library(lavaan)')
    ro.r.assign("modelo", model_desc)
    ro.r.assign("caminho_csv", str(csv_path))

    ro.r('''
    dados1 <- read.csv(caminho_csv, stringsAsFactors = FALSE)
    dados1 <- na.omit(dados1)
    dados1[] <- lapply(dados1, function(x) as.numeric(as.character(x)))
    ''')

    if ordered_vars:
        ro.globalenv['ordered_vars'] = StrVector(ordered_vars)
        ro.r(f'''
        fit <- sem(model = modelo, data = dados1, ordered = ordered_vars, estimator = "{estimator}")
        ''')
    else:
        ro.r(f'''
        fit <- sem(model = modelo, data = dados1, estimator = "{estimator}")
        ''')

    if not bool(ro.r('lavInspect(fit, "converged")')[0]):
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
