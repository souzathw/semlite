import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

def run_lavaan_sem(model_desc, df, estimator="WLSMV", ordered_vars=None):
    try:
        ro.r('library(lavaan)')
    except Exception as e:
        raise RuntimeError(f"❌ Erro ao carregar o pacote lavaan no R: {e}")

    with localconverter(pandas2ri.converter):
        r_df = pandas2ri.py2rpy(df)

    ro.globalenv['dados1'] = r_df
    ro.globalenv['modelo'] = model_desc

    if ordered_vars:
        ro.globalenv['ordered_vars'] = ro.StrVector(ordered_vars)
        ordered_arg = 'ordered=ordered_vars,'
    else:
        ordered_arg = ''

    ro.r(f"""
    fit <- sem(
      model = modelo,
      data = dados1,
      {ordered_arg}
      estimator = '{estimator}',
      fixed.x = FALSE,
      std.lv = TRUE,
      check.gradient = FALSE,
      start = 'simple',
      control = list(rel.tol = 1e-5, max.iter = 10000)
    )

    indices <- fitMeasures(fit, c('chisq', 'df', 'cfi', 'tli', 'rmsea', 'rmsea.ci.lower', 'rmsea.ci.upper', 'srmr'))
    estimates <- parameterEstimates(fit, standardized = TRUE)
    resumo <- capture.output(summary(fit, standardized = TRUE))
    """)

    with localconverter(pandas2ri.converter):
        estimates_df = ro.r('estimates')

    indices = dict(zip(ro.r('names(indices)'), list(ro.r('indices'))))
    summary_out = list(ro.r('resumo'))

    return {
        "indices": indices,
        "estimates": estimates_df,
        "summary": summary_out
    }
