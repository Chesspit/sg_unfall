import dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pathlib   

token = open(".env").read()
# print(token)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("assets").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("unfallorte.csv"))

# Hilfsvariablen
monate = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']

# Components

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title"),
            html.P(
                "Some quick example text to build on the card title and make "
                "up the bulk of the card's content.",
                className="card-text",
            ),
        ]
    ),
)


cl_all = dbc.Card(
            [   
                dbc.CardBody(
                    [
                    html.H4("Einstellung Unfallparameter", className="card-title"),
                    html.H6("Typ", className="card-title"),
                    dbc.Checklist(
                                id="checklist_typ",
                                options=[
                                    {"label": x, "value": x}
                                    for x in sorted(df["Unfalltyp"].unique())],
                                value=["Fussgängerunfall", "Abbiegeunfall"],
                                inline=True
                        )
                    ]
                ),
               dbc.CardBody(
                    [
                    html.H6("Schwere", className="card-title"),
                    dbc.Checklist(
                            id="checklist_schwere",
                            options=[{'label': item, 'value': item} for item in df["Unfallschwere"].unique()],
                            value=["Unfall mit Schwerverletzten"],
                            inline = True                         
                        )
                    ]
                ),
               dbc.CardBody(
                    [
                    html.H6("Beteiligte", className="card-title"),
                    dbc.Checklist(id="checklist_beteiligte",
                        options=[
                                {'label': 'Fussgänger', 'value': 'Fussgänger'},
                                {'label': 'Fahrrad', 'value': 'Fahrrad'},
                                {'label': 'Motorrad', 'value': 'Motorrad'},
                        ],
                        value=['Fussgänger'],
                        inline=True                         
                        )
                    ]
                ),                       
               dbc.CardBody(
                    [
                    html.H6("Strassentyp", className="card-title"),
                    dbc.Checklist(id="checklist_strasse",
                        options=[
                                {'label': 'Autobahn', 'value': 'Autobahn'},
                                {'label': 'Hauptstrasse', 'value': 'Hauptstrasse'},
                                {'label': 'Nebenstrasse', 'value': 'Nebenstrasse'},
                                {'label': 'andere', 'value': 'andere'},
                        ],
                        value=['Hauptstrasse'],
                        inline=True                      
                        )
                    ]
                )
            ],
    body=True,
    className="mt-4",  
    # style={"height": "5rem"}
)


slider_card_start = dbc.Card(
    [
        html.H6("Start Datum", className="card-title"),
        dcc.Slider(
            id="start_monat",
            marks=dict(zip(range(1, 13, 1), monate)),
            # marks={i: f"{i}" for i in monate},
            min=1,
            max=12,
            step=1,
            value=5,
            included=False,
        ),
        dcc.Slider(
            id="start_jahr",
            marks={i: f"{i}" for i in range(2011, 2023, 1)},
            min=2011,
            max=2022,
            step=1,
            value=2015,
            included=False,
        ),
    ],
    body=True,
    className="mt-4",
)

slider_card_ende = dbc.Card(
    [
        html.H6("Ende Datum", className="card-title"),
        dcc.Slider(
            id="ende_monat",
            marks=dict(zip(range(1, 13, 1), monate)),
            min=1,
            max=12,
            step=1,
            value=9,
            included=False,
        ),
        dcc.Slider(
            id="ende_jahr",
            marks={i: f"{i}" for i in range(2011, 2023, 1)},
            min=2011,
            max=2022,
            step=1,
            value=2019,
            included=False,
        ),
    ],
    body=True,
    className="mt-4",
)

footer = html.Div(
    [
        dcc.Markdown(
            """
             XXX            
            """
        ),

    ],
    className="p-2 mt-5 bg-primary text-white small",
)


# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Verkehrsunfallorte im Kanton St. Gallen",
                    className="text-center bg-primary text-white p-2",
                ),
            )
        ),
        dbc.Row(
                [
                dbc.Col(card, width=12, lg=4, className="mt-4 border"),
                dbc.Col([html.P("Häufigkeit nach Wochentag und Stunde"),
                    html.Div(id="table_sg")   
                         ]),
                ],
                className="ms-1",
                ),
        dbc.Row(
                [
                    dbc.Col([cl_all, 
                                slider_card_start, slider_card_ende], 
                                width=12, lg=4, className="mt-4 border"),
                    dbc.Col(dcc.Graph(id="map_sg"), width=12, lg=8, className="mt-4 border"),
                ],
                className="ms-1",
                ),
        dbc.Row(dbc.Col(footer)),
    ],
    fluid=True,
)

# functions
def filter_df(checklist_typ, checklist_schwere, checklist_beteiligte, checklist_strasse, start_monat, start_jahr, ende_monat, ende_jahr):
    # Ich filtere mal etwas "unfachmässig" in 3 Schritten
    start = pd.to_datetime(str(start_jahr) + '-' + str(start_monat) + '-01')
    start = start.strftime('%Y-%m-%d')
    ende = pd.to_datetime(str(ende_jahr) + '-' + str(ende_monat) + '-01')
    ende = ende.strftime('%Y-%m-%d')
    df_filtered = df.query('@start <= Datum <= @ende')

    # Hier folgt ein 2. Filter auf Basis der Unfallbeteiligung. Basis sind 3 Spalten mit Boolean Values, dh True bzw. False
    beteiligte = ' or '.join([f'{col} == True' for col in checklist_beteiligte])
    df_filtered = df_filtered.query(beteiligte)

    # Im letzten Schritt werden Unfalltyp, Unfallschwere und Strassentyp berücksichtigt 
    # print(checklist_typ, checklist_schwere, checklist_strasse)
    df_filtered = df_filtered.query('Unfalltyp in @checklist_typ and Unfallschwere in @checklist_schwere and Strassentyp in @checklist_strasse')
    return df_filtered


# Callbacks

@app.callback(
    Output("map_sg", "figure"),
    Input("checklist_typ", "value"),
    Input("checklist_schwere", "value"),
    Input("checklist_beteiligte", "value"),
    Input("checklist_strasse", "value"),
    Input("start_monat", "value"),
    Input("start_jahr", "value"),
    Input("ende_monat", "value"),
    Input("ende_jahr", "value"),    
)
def fig_update(checklist_typ, checklist_schwere, checklist_beteiligte, checklist_strasse, start_monat, start_jahr, ende_monat, ende_jahr):
    df_filtered = filter_df(checklist_typ, checklist_schwere, checklist_beteiligte, checklist_strasse, start_monat, start_jahr, ende_monat, ende_jahr)

    fig = px.scatter_mapbox(df_filtered, lat="Breitengrad", lon="Längengrad", color=df_filtered['Unfallschwere'],
                                    opacity=0.99, zoom=11.5)
    fig.update_layout(mapbox_style="streets", mapbox_accesstoken=token,
                            legend = dict(bgcolor = '#F5F5F5', title_text=''))
    return fig

@app.callback(
    Output("table_sg", "children"),
    Input("checklist_typ", "value"),
    Input("checklist_schwere", "value"),
    Input("checklist_beteiligte", "value"),
    Input("checklist_strasse", "value"),
    Input("start_monat", "value"),
    Input("start_jahr", "value"),
    Input("ende_monat", "value"),
    Input("ende_jahr", "value"),    
    )
def table_update(checklist_typ, checklist_schwere, checklist_beteiligte, checklist_strasse, start_monat, start_jahr, ende_monat, ende_jahr):
    df_weekday_hour = pd.pivot_table(df, values="Unfalltyp", index='Wochentag', columns='Stunde', aggfunc='size', fill_value=0)
    # If needed, reset the index to make 'Wochentag' a column again
    df_weekday_hour = df_weekday_hour.reset_index()
    # Die DataTable benötigt Spaltenköpfe vom Typ STRING
    df_weekday_hour.columns = df_weekday_hour.columns.astype(str)
    data = df_weekday_hour.to_dict('records')
    columns =  [{"name": i, "id": i} for i in df_weekday_hour.columns]
    return dash_table.DataTable(data=data, columns=columns)


if __name__ == '__main__':
    app.run_server(debug=True, port = 8055)