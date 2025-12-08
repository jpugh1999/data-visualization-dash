import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv('fl_city_counts.csv')

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='City Record Bubble Map Dashboard'),
    html.Div(children='Filter by City:'),
    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': i, 'value': i} for i in df['Petitioner City'].unique()
        ]
        + [{'label':'All States', 'value':'ALL'}],
        value='ALL',
        clearable=True
    ),
    dcc.Graph(
        id='city-state-map',
        style={'height': '80vh'}
    )
])

@app.callback(
    Output('city-state-map', 'figure'),
    [Input('city-dropdown', 'value')]
)

def update_graph(selected_city):
    if selected_city == 'ALL':
        filtered_df = df
    else:
        filtered_df = df[df['Petitioner City']==selected_city]

    fig = px.scatter_map(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        hover_name='Petitioner City',
        size='Petition Count',
        size_max=80,
        color='Petition Count',
        title='H1B Petition Counts by City in Florida',
        color_continuous_scale=px.colors.sequential.Plasma,
        zoom=6.5, # Set zoom level appropriate for Florida (5-8 is usually good)
        center={"lat": 28.0, "lon": -82.0}, # Center the map on Florida
        map_style="open-street-map"
    )

    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)