from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata

df = px.data.gapminder()


countries = df["country"].drop_duplicates()

app = Dash(__name__)

server = app.server

app.layout = html.Div(
    children=[
        html.H1("GDP per Capita Growth Explorer"),
        html.Label("Select a country:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in countries],
            value="Canada",
            clearable=False
        ),
        dcc.Graph(id="gdp-growth")
    ],
    style={"maxWidth": "900px", "margin": "0 auto"}
)

@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value")
)

def update_graph(country_name: str):
    filtered_df = df[df["country"]==country_name]

    fig = px.line(
        filtered_df,
        x="year",
        y="gdpPercap",
        title=f"GDP per Capita Over Time: {country_name}",
        labels={"year": "Year", "gdpPercap": "GDP per Capita"}
    )

    return fig

if __name__=="__main__":
    app.run(debug=True)