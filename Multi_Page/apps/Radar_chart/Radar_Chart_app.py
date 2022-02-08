# ------------------------------------------------Imports------------------------------------------------------------- #

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os
from Multi_Page.StartingBusiness import app

pio.renderers.default = "browser"

# -----------------------------------------------StyleSheet----------------------------------------------------------- #

external_stylesheets = [dbc.themes.COSMO]

# ------------------------------------------------Data&Lists---------------------------------------------------------- #
# Import data from the correct directory and add lists for dropdown menus
df_path = os.path.join("apps", "Radar_chart")
df_radar = pd.read_csv(os.path.join(df_path, "DBRadar.csv"))
country_list = df_radar['Country Name'].unique().tolist()
year_list = list(range(2006, 2021))

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# -------------------------------------------Web Page Style----------------------------------------------------------- #
# Creating the container as two columns of different widths to incorporate 2 radar charts, with 2 dropdown menus each. 
# Disabled the multi selection function for dropdowns.

radar_page = dbc.Container(fluid=True, children=[
    dbc.Row(
        dbc.Col(children=[html.Br()])),

    dbc.Row([
        dbc.Col(width=6, children=[
            dcc.Graph(id="radar_chart"),
        ]),
        dbc.Col(width=6, children=[
            dcc.Graph(id="radar_chart1"),
        ]),
    ]),

    dbc.Row([
        dbc.Col(width={"size":3, "offset": 1}, children=[
            html.Br(),
            html.H5('Select Country'),
            dcc.Dropdown(
                options=[{"label": x, "value": x}
                         for x in country_list],
                value=[],
                id="country",
                multi=False, 
            ),
            html.H5('Select Year'),
            dcc.Dropdown(
                options=[{"label": x, "value": x}
                         for x in year_list],
                value=[],
                id="year",
                multi=False,
            ),
            html.Br(),
        ]),
        dbc.Col(width={"size":3, "offset": 3}, children=[
            html.Br(),
            html.H5('Select Country'),
            dcc.Dropdown(
                options=[{"label": x, "value": x}
                         for x in country_list],
                value=[],
                id="country1",
                multi=False,
            ),
            html.H5('Select Year'),
            dcc.Dropdown(
                options=[{"label": x, "value": x}
                         for x in year_list],
                value=[],
                id="year1",
                multi=False,
            ),
            html.Br(),
        ]),
    ]),
])

# -----------------------------------------------Layout--------------------------------------------------------------- #
# Generating app layout based on container

app.layout = radar_page

# -------------------------------------------Interactivity and Charts------------------------------------------------- #
# Generating and updating the 2 radar charts (lis_fig[0] and lis_fig[1]) capturing the user inputs generated by
# selecting values in the different dropdown menus. 

@app.callback(
    [Output("radar_chart", "figure"), Output("radar_chart1", "figure")],
    [Input("country", "value")], [Input("year", "value")],
     [Input("country1", "value")], [Input("year1", "value")])
def update_chart(country, year, country1, year1):
    # Storing default values when nothing is selected in the dropdown menu
    if isinstance(country, list):
        if len(country) == 0:
            country = 'Afghanistan'
    else:
        if country == '':
            country = 'Afghanistan'
    if isinstance(country1, list):
        if len(country1) == 0:
            country1 = 'Afghanistan'
    else:
        if country1 == '':
            country1 = 'Afghanistan'
    if isinstance(year, int):
        if year == '':
            year = '2019'
    else:
        if len(year) == 0:
            year = '2019'
    if isinstance(year1, int):
        if year1 == '':
            year1 = '2020'
    else:
        if len(year1) == 0:
            year1 = '2020'

    # Creating lists to store selected dropdown value and figure
    lis1 = [str(country), str(country1)]
    lis2 = [str(year), str(year1)]
    lis_fig = []
    indicators_title = ['Time required score','Procedures required score',
    'Cost (% of income per capita) score']

    for i in range(len(lis1)):
        year = lis2[i]
        country = lis1[i]

        # Accessing the dataframe indexes for each indicator depending 
        # on selected counntry and year
        header = df_radar.columns.tolist()
        col = header.index(year)
        row = country_list.index(country)
        afg_idx = df_radar.index[df_radar['Country Name']
         == df_radar.iloc[0, 0]].tolist()

        # Accessing the scores for each indicator
        radar_m = [df_radar.iloc[afg_idx[0]+row, col],
         df_radar.iloc[afg_idx[2]+row, col], df_radar.iloc[afg_idx[4]+row, col]]
        radar_w = [df_radar.iloc[afg_idx[1]+row, col],
         df_radar.iloc[afg_idx[3]+row, col], df_radar.iloc[afg_idx[5]+row, col]]

        # Generating figure with two radar plots superimposed
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=radar_m,
            theta=indicators_title,
            line_color='blue',
            fill='toself',
            name=f'Men'
        ))

        fig.add_trace(go.Scatterpolar(
            r=radar_w,
            theta=indicators_title,
            line_color='red',
            fill='toself',
            name=f'Women'
        ))

        fig.update_layout(
            title_text= f'Scores for setting up a business according to gender in {df_radar.iloc[0+row,0]} in {header[col]}',
            title_x=0.5,
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 100]
                )))

        fig.layout.autosize = True
        lis_fig.append(fig)

    return lis_fig[0], lis_fig[1]


if __name__ == '__main__':
    app.run_server(debug=True)