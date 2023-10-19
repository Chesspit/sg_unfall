import dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import pathlib   

# Da die App via RENDER deployed wird, erfolgt der Zugriff auf den Token via .yaml-File
# mapbox_token = open(".env").read()
# print(token)
# import os
# mapbox_token = os.environ.get('mapbox_token')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("assets").resolve()

# Read data
df = pd.read_csv(DATA_PATH.joinpath("unfallorte.csv"))

# Hilfsvariablen
monate = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
wtage = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

# # Mapping der Strings in den Spalten, um kürzere Strings für die Paramenterwahl zu haben
mapping_dict_typ = {
    'Abbiegeunfall': 'Abbiege',
    'Auffahrunfall': 'Auffahr',
    'Andere': 'Andere',
    'Einbiegeunfall': 'Einbiege',
    'Frontalkollision': 'Frontal',
    'Fussgängerunfall': 'Fussgänger',
    'Parkierunfall': 'Parkier',
    'Schleuder- oder Selbstunfall': 'Schleuder',
    'Tierunfall': 'Tier',
    'Überholunfall oder Fahrstreifenwechsel': 'Überholunfall',
    'Überqueren der Fahrbahn': 'Fahrbahnüberquerung',
}
df['Unfalltyp'] = df['Unfalltyp'].map(mapping_dict_typ)

mapping_dict_schwere = {
    'Unfall mit Leichtverletzten': 'Leicht',
    'Unfall mit Schwerverletzten': 'Schwer',
    'Unfall mit Getöteten': 'Getötete',
}
df['Unfallschwere'] = df['Unfallschwere'].map(mapping_dict_schwere)


# Components

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Information und Anleitung", className="card-title"),
            html.P(
                """Diese interaktive Auswertung basiert auf der öffentlich verfügbaren 
                Datenbasis von 2011 bis 2022. Zeitraum und ebenso die Charakteristika
                der Unfälle können weiter unten individuell eingestellt werden. 
                Die Tabelle zeigt die Einordnung der Unfälle nach Wochentag und Stunde 
                des Tages.
                Die Grafik zeigt die Orte, an denen die Unfälle passiert sind.""",
                className="card-text"),
            #  html.H4("Einstellung Unfallparameter", className="card-title"),
        ]
    ),
)


cl_all = dbc.Card(
            [   
                dbc.CardBody(
                    [
                    # html.H4("Einstellung Unfallparameter", className="card-title"),
                    html.H6("Typ des Unfalls", className="card-title"),
                    dbc.Checklist(
                                id="checklist_typ",
                                options=[{'label': item, 'value': item} for item in df["Unfalltyp"].unique()],   
                                value=["Fussgänger", "Abbiege", "Auffahr"],
                                inline=True
                        )
                    ],
                    style={"height": "7rem"},

                ),
               dbc.CardBody(
                    [
                    html.H6("Schwere der Verletzung", className="card-title"),
                    dbc.Checklist(
                            id="checklist_schwere",
                            options=[{'label': item, 'value': item} for item in df["Unfallschwere"].unique()],
                            value=["Leicht", "Schwer", "Getötete"],
                            inline = True                         
                        )
                    ],
                    style={"height": "4rem"},                    
                ),
               dbc.CardBody(
                    [
                    html.H6("Beteiligte am Unfall", className="card-title"),
                    dbc.Checklist(id="checklist_beteiligte",
                        options=[
                                {'label': 'Fussgänger', 'value': 'Fussgänger'},
                                {'label': 'Fahrrad', 'value': 'Fahrrad'},
                                {'label': 'Motorrad', 'value': 'Motorrad'},
                        ],
                        value=['Fussgänger', 'Fahrrad'],
                        inline=True                         
                        )
                    ],
                    style={"height": "4rem"},
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
                        value=["Autobahn", 'Hauptstrasse'],
                        inline=True                      
                        )
                    ],
                    style={"height": "4rem"},
                )
            ],
    body=True,
)


slider_card_start = dbc.Card(
    [
        html.H6("Start", className="card-title"),
        dcc.Slider(
            id="start_monat",
            marks=dict(zip(range(1, 13, 1), monate)),
            # marks={i: f"{i}" for i in monate},
            min=1,
            max=12,
            step=1,
            value=4,
            included=False,
        ),
        dcc.Slider(
            id="start_jahr",
            marks={i: f"{i}" for i in range(2011, 2023, 1)},
            min=2011,
            max=2022,
            step=1,
            value=2012,
            included=False,
        ),
    ],
    body=True,
    className="mt-4",
)

slider_card_ende = dbc.Card(
    [
        html.H6("Ende", className="card-title"),
        dcc.Slider(
            id="ende_monat",
            marks=dict(zip(range(1, 13, 1), monate)),
            min=1,
            max=12,
            step=1,
            value=10,
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


# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Verkehrsunfallorte in St. Gallen",
                    className="text-center bg-primary text-white p-2 mb-6",
                ),
            ),
            className=" mb-3"
        ),
        dbc.Row(
                [
                dbc.Col(card, width=12, lg=4, className="mt-4 "),
                dbc.Col([html.H6("Häufigkeit nach Wochentag und Stunde"),
                    html.Div(id="table_sg")   
                         ]),
                ],
                className="ms-1",
                ),
        dbc.Row(
                [
                    dbc.Col([cl_all, 
                                slider_card_start, slider_card_ende], 
                                width=12, lg=4, className="mt-4"),
                    dbc.Col(dcc.Graph(id="map_sg"), width=12, lg=8, className="mt-4 border"),
                ],
                className="ms-1",
                ),
        # dbc.Row(dbc.Col(footer)),
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

    fig = px.scatter_mapbox(df_filtered, lat="Breitengrad", lon="Längengrad", 
                            color=df_filtered['Unfallschwere'], color_discrete_map={"Leicht": "green", "Schwer": "orange", "Getötete": "red"},
                                    opacity=0.99, zoom=12, width=1200, height=700,
                                    hover_data={'Längengrad':False, 'Breitengrad':False, 'Unfallschwere':False, 
                                                'Unfalltyp': True, 'Jahr': True, 'Monat': True, 'Wochentag': True, 'Stunde': True
                                    })                     
    fig.update_layout(mapbox_style="streets", mapbox_accesstoken = mapbox_token,
                            legend = dict(bgcolor = '#F5F5F5', title_text='Schwere der Verletzung', x=0.02, y=1.02, orientation="h", yanchor='bottom'),
                            )    
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
    df_filtered = filter_df(checklist_typ, checklist_schwere, checklist_beteiligte, checklist_strasse, start_monat, start_jahr, ende_monat, ende_jahr)
    # In den nächsten beiden Zeilen sorge ich noch dafür, dass von MO nach SO sortiert wird
    df_filtered['Wochentag'] = pd.Categorical(df_filtered['Wochentag'],categories=wtage)
    df_filtered = df_filtered.sort_values('Wochentag') 
    df_weekday_hour = pd.pivot_table(df_filtered, values="Unfalltyp", index='Wochentag', columns='Stunde', aggfunc='size', fill_value=0)
    # print(df_weekday_hour)
    # If needed, reset the index to make 'Wochentag' a column again
    df_weekday_hour = df_weekday_hour.reset_index()
    # Die DataTable benötigt Spaltenköpfe vom Typ STRING
    df_weekday_hour.columns = df_weekday_hour.columns.astype(str)
    df_weekday_hour_new = df_weekday_hour.iloc[:, 0:23] 
    # print(df_weekday_hour_new)
    # print(df_weekday_hour_new.columns)
    data = df_weekday_hour_new.to_dict('records')
    # print(data)
    columns =  [{"name": i, "id": i} for i in df_weekday_hour_new.columns]
    # print("Spalten")
    print(columns)
    table_sg = dash_table.DataTable(
        data=data, 
        columns=columns,
        style_cell={
            'width': '7px',
            'maxWidth': '7px',
            'minWidth': '7px',
            'textAlign': 'center',  
        },
        style_header={'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',               
            },
        ] ,  
        style_cell_conditional=[
            {
                'if': {'column_id': 'Wochentag'},
                'width': '15%'
            },
        ]   
        )


    return table_sg
    # return dash_table.DataTable(data=data, columns=columns)


if __name__ == '__main__':
    app.run_server(debug=True, port = 8056)
