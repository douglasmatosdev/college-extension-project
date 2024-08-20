import plotly.express as px
import pandas as pd

df = pd.read_excel("../datasource/eletrecidade.xlsx")

fig = px.bar(
    df,
    x="Referência",
    y="Valor",
    title="Gastos com Eletrecidade de 2021 à 2024",
    labels={"Valor": "Valor (R$)", "Referência": "Meses/Ano"},
)

fig.show()
