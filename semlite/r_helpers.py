import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import default_converter
from rpy2.robjects.pandas2ri import py2rpy, rpy2py_dataframe

ro.r('library(lavaan)')

def run_lavaan_sem(model_desc, csv_path, estimator="WLSMV", ordered_vars=None):
    df = pandas2ri.read_csv(csv_path)

    with localconverter(default_converter + pandas2ri.converter):
        r_df = py2rpy(df)

    ro.globalenv['dados1'] = r_df
    ro.globalenv['modelo'] = model_desc

    ro.r('dados1 <- na.omit(dados1)')

    if ordered_vars is not None:
        ro.globalenv['ordered_vars'] = ro.StrVector(ordered_vars)
        ro.r(f'''
        fit <- sem(model=modelo, data=dados1, ordered=ordered_vars, estimator="{estimator}")
        ''')
    else:
        ro.r(f'''
        fit <- sem(model=modelo, data=dados1, estimator="{estimator}")
        ''')

    ro.r('''
    indices <- fitMeasures(fit, c("chisq", "df", "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))
    estimates <- parameterEstimates(fit, standardized=TRUE)
    resumo <- capture.output(summary(fit, standardized=TRUE))
    ''')

    indices = dict(zip(ro.r('names(indices)'), list(ro.r('indices'))))

    with localconverter(default_converter + pandas2ri.converter):
        estimates_df = rpy2py_dataframe(ro.r('estimates'))
        resumo = list(ro.r('resumo'))

    return {
        "indices": indices,
        "estimates": estimates_df,
        "summary": resumo
    }
