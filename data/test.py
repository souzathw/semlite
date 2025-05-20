import pandas as pd
from semopy import Model

df = pd.read_csv("teste_cfa_simulado.csv", sep=';')

model_desc = "DF =~ DF1 + DF2 + DF3 + DF4"
model = Model(model_desc)
model.fit(df)

print(model.inspect(std_est=True))
print(model.calc_stats())
