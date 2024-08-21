from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

dataset = pd.read_excel("./datasource/eletrecidade.xlsx")

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1('Projeto de extensão'),
    html.P("Selecione o mês:"),
    dcc.Dropdown(
        id="dropdown",
        options=dataset["Referência"].unique(),
        value='Gold',
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def display_color(month):
    fig = px.bar(
    dataset,
    x="Referência",
    y="Valor",
    title="Gastos com Eletrecidade de 2021 à 2024",
    labels={"Valor": "Valor (R$)", "Referência": "Meses/Ano"},
)
    return fig


app.run_server(debug=True)


# fig = px.bar(
#     dataset,
#     x="Referência",
#     y="Valor",
#     title="Gastos com Eletrecidade de 2021 à 2024",
#     labels={"Valor": "Valor (R$)", "Referência": "Meses/Ano"},
# )

# fig.show()
