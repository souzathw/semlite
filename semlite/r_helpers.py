import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

pandas2ri.activate()

ro.r('library(lavaan)')

def run_lavaan_sem(model_desc, df, estimator="WLSMV"):
    r_df = pandas2ri.py2rpy(df)
    ro.globalenv['dados1'] = r_df
    ro.globalenv['modelo'] = model_desc

    ro.r(f'''
    fit <- sem(model=modelo, data=dados1, ordered=colnames(dados1), estimator="{estimator}")
    indices <- fitMeasures(fit, c("chisq", "df", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
    estimates <- parameterEstimates(fit, standardized=TRUE)
    ''')

    indices = dict(zip(ro.r('names(indices)'), list(ro.r('indices'))))

    estimates_r = ro.r('estimates')
    estimates_df = pandas2ri.rpy2py(estimates_r)

    return indices, estimates_df
