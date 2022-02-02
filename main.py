from dash import Dash, Input, Output
from dash import dash_table as dt
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
import os
import pathlib

# Start app.
app = Dash()
app.title = "Learning python."

# Load data.
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

df_player_board = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "players.csv")))
df_player_board.columns = ['player_pubkey', 'fire', 'water', 'nature', 'team']
df_map = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "map.csv")))
df_map.columns = ['host_pubkey', 'row', 'column', 'fire', 'water', 'nature', 'biome']



# Build map.
def build_map(original_df):
    data = {'A': ['team0A', 'team1A', 'team2A', 'team3A'],
            'B': ['team0B', 'team1B', 'team2B', 'team3B'],
            'C': ['team0C', 'team1C', 'team2C', 'team3C'],
            'D': ['team0D', 'team1D', 'team2D', 'team3D'],
            }
    new_df = pd.DataFrame(data)
    # foreach row
    for index, row in original_df.iterrows():
        r = row['row']
        c = row['column']
        b = row['biome']
        new_df.iloc[r, c] = b
    return new_df


# Convert map dataframe.
df_map = build_map(df_map)

# Define layout.
app.layout = html.Div(
    id="app-container",
    children=[
    # Player card.
    html.P("PLAYER NAME"),

    # Player board.
    dt.DataTable(
        id='player-board',
        data=df_player_board.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_player_board.columns],
    ),

    # Character details
    dcc.Graph(
        id="pie-chart"
    ),

    # World map.
    dt.DataTable(
        id='world-map',
        data=df_map.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_map.columns],
    ),

    # Region details.
    html.Img(id='image'),

    # Engage button.
    html.Button(
        'Engage',
        id="engage-button",
        n_clicks=0
    ),
    html.Label(
        id="engage-label"
    ),
    # Subscription timer.

])

# Handlers.
@app.callback(
    Output("pie-chart", "figure"),
    [Input('player-board', 'active_cell')]
)
def generate_chart(data):
    names_list = ['fire', 'water', 'nature']
    values_list = [0, 0, 0]
    if data is not None:
        row = data["row"]
        dfpie = df_player_board.iloc[row, 1:4].to_frame()
        dfpie.columns = ['count']
        values_list = list(dfpie['count'])

    fig = px.pie(None, values=values_list, names=names_list)
    return fig

# Engage Button.
@app.callback(
    Output('engage-label', 'children'),
    Input('engage-button', 'n_clicks')
)
def update_output(n_clicks):
    return 'The input value was MISSING and the button has been clicked {} times'.format(
        n_clicks
    )

# Image.
@app.callback(
    Output('image', 'src'),
    [Input('world-map', 'active_cell')]
)
def update_image_src(value):
    if df_map is not None and value is not None:
        biome = df_map.iloc[value['row']][value['column']]
        return '/assets/'+biome+'.jpg'
    return '/assets/dash-logo-new.png'


# Main run.
if __name__ == "__main__":
    app.run_server(debug=True)
