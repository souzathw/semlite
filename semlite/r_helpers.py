import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.pandas2ri import rpy2py

# Carrega o lavaan uma vez
ro.r('library(lavaan)')

def run_lavaan_sem(model_desc, csv_path, estimator="ML", ordered_vars=None):
    ro.r(f'dados1 <- read.csv("{csv_path}")')
    ro.r('dados1 <- na.omit(dados1)') 
    ro.globalenv['modelo'] = model_desc

    if ordered_vars:
        ro.globalenv['ordered_vars'] = ro.StrVector(ordered_vars)
        ro.r(f'''
            fit <- sem(model=modelo, data=dados1, estimator="{estimator}", ordered=ordered_vars)
        ''')
    else:
        ro.r(f'''
            fit <- sem(model=modelo, data=dados1, estimator="{estimator}")
        ''')

    ro.r('''
        indices <- fitMeasures(fit, c("chisq", "df", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
        estimates <- parameterEstimates(fit, standardized=TRUE)
        resumo <- capture.output(summary(fit, fit.measures=TRUE, standardized=TRUE))
    ''')

    with localconverter(ro.default_converter + pandas2ri.converter):
        estimates_df = rpy2py(ro.r('estimates'))

    indices = dict(zip(ro.r('names(indices)'), list(ro.r('indices'))))
    resumo = list(ro.r('resumo'))

    return {
        "indices": indices,
        "estimates": estimates_df,
        "summary": resumo
    }
