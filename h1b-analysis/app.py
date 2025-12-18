import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

df = pd.read_csv('fl_city_counts.csv')
df_full = pd.read_csv('fl_h1b_data.csv')
df_full = df_full[['Fiscal Year', 
         'Employer (Petitioner) Name', 
         'Tax ID', 'Industry (NAICS) Code', 
         'Petitioner City', 
         'Petitioner State', 
         'Petitioner Zip Code',
         'Total_Approvals',
         'New Employment Approval',
         'New Employment Denial', 
         'Continuation Approval', 
         'Continuation Denial',
         'Change with Same Employer Approval',
         'Change with Same Employer Denial', 
         'New Concurrent Approval', 
         'New Concurrent Denial', 
         'Change of Employer Approval',
         'Change of Employer Denial', 
         'Amended Approval', 
         'Amended Denial'
         ]]
df_full = df_full.sort_values(by=['Fiscal Year', 'Total_Approvals', 'Tax ID'], ascending=False)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    ),
    html.Div(
        id='click-data-output',
        style={'padding':'10px'}
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
        size='Total Approvals',
        size_max=80,
        color='Total Approvals',
        title='H1B Approvals by City in Florida',
        color_continuous_scale=px.colors.sequential.Plasma,
        zoom=6.5, # Set zoom level appropriate for Florida (5-8 is usually good)
        center={"lat": 28.0, "lon": -82.0}, # Center the map on Florida
        map_style="open-street-map"
    )

    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    return fig

@app.callback(
    Output('click-data-output', 'children'),
    [Input('city-state-map', 'clickData')]
)
def display_click_data(clickData):
    if clickData is None:
        return html.Div("Click a bubble on the map to display it's details")
    
    point = clickData['points'][0]

    city = point.get('hovertext', 'N/A')
    count = point.get('marker.size', 'N/A')

    city_df = df_full[df_full['Petitioner City'] == city]

    return html.Div([
        html.H3(f"Details for: {city}"),
        dash_table.DataTable(
            id='city-details-table',
            data = city_df.to_dict('records'),
            columns=[
                {"name": i, "id": i} for i in city_df.columns
            ],
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'},
            page_action='none'
        )
    ])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)