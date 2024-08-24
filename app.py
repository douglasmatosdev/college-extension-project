from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

data_eletricidade = pd.read_excel("./datasource/eletricidade.xlsx")
data_internet= pd.read_excel("./datasource/internet.xlsx")
data_scraped = pd.read_csv("./datasource/data_scraped.csv")

app = Dash(__name__)

server = app.server

figEletricidade = px.bar(
    data_eletricidade,
    x="Referência",
    y="Valor",
    title="Gastos com Eletricidade de 2021 à 2024",
    labels={"Valor": "Valor (R$)", "Referência": "Meses/Ano"},
)

figInternet = px.bar(
    data_internet,
    x="PERÍODO",
    y="VALOR",
    title="Gastos com Internet de 2022 à 2024",
    labels={"VALOR": "Valor (R$)", "PERÍODO": "Meses/Ano"},
)

figDataScraped = px.bar(data_scraped, title="Reações em posts do Facebook", labels={"value": "Quantidade", "variable": "Livros"})

app.layout = html.Div([
    html.H1('Projeto de extensão'),
    dcc.Graph(
        id="graph_eletricidade",
        figure=figEletricidade
    ),
    dcc.Graph(
        id="graph_internet",
        figure=figInternet
    ),
    dcc.Graph(
        id="graph_data_scraped",
        figure=figDataScraped
    )
])

app.run_server(debug=True, port=8050, host='0.0.0.0')