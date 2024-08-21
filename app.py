from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

data_eletrecidade = pd.read_excel("./datasource/eletrecidade.xlsx")

app = Dash(__name__)

server = app.server


fig = px.bar(
    data_eletrecidade,
    x="Referência",
    y="Valor",
    title="Gastos com Eletrecidade de 2021 à 2024",
    labels={"Valor": "Valor (R$)", "Referência": "Meses/Ano"},
)


app.layout = html.Div([
    html.H1('Projeto de extensão'),
    dcc.Graph(
        id="graph",
        figure=fig
    ),
])



app.run_server(debug=True)