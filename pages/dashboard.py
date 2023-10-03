from dash import html
from dash import dcc
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import json
import pandas as pd
import functions
from dash import callback
from dash import ctx

dash.register_page(__name__, path='/',
                   name='Dashboard Werknemers Nederland')  # registering the page to connect to main page

date_header = html.Div(["Gebaseerd op data tot 31-12-2022",html.Br()], id = 'date-header')
link = 'https://opendata.cbs.nl/portal.html?_la=nl&_catalog=CBS&tableId=81431ned&_theme=6'
source = html.Div(["bron: ", dcc.Link('CBS Open Data Statline', href=link, target="_blank")], id='source-link')
dashboardheader = html.Div([date_header, source],  id = 'dash-header')

worksum = pd.read_csv('data/worksum.csv')
description = pd.read_csv('data/description.csv')['Description']

# Creating all the dropdowns for the dashboard

columnsp = ['Aantal Banen', 'Arbeidsvolume', 'Gemiddeld uren werk per jaar', 'Uurloon', 'Jaarloon']
parameterlabels = [{'label': k, 'value': k} for k in columnsp]
parameterdropdown = dcc.Dropdown(id='parameter-picker', options=parameterlabels,
                                 value='Aantal Banen', clearable=False, className='dropdown')

sectordict = dict(zip(worksum.Bedrijfstak.unique(), worksum.Bedrijfstak.unique()))
sectorlabels = [{'label': k, 'value': v} for k, v in sectordict.items()]
industrydropdown = dcc.Dropdown(id='industry-picker', options=sectorlabels, clearable=False,
                                value='A-U Alle economische activiteiten', className='dropdown')

catdict = {'Totaal': 1, 'Geslacht': 6, 'Leeftijd': 7, 'Dienstverband': 2, 'Arbeidsduur': 3, 'Bedrijfsomvang': 10,
           'Sector': 11}
catlabels = [{'label': k, 'value': k} for k, v in catdict.items()]
catdropdown = dcc.Dropdown(id='category-picker', options=catlabels, clearable=False,
                           value='Geslacht', className='dropdown')

labels = worksum[worksum.CategoryGroupID_Kenmerken == 6]['Kenmerken'].unique()
speclabels = [{'label': k, 'value': k} for k in labels]
specdropdown = dcc.Dropdown(id='spec-picker', options=speclabels, className='dropdown', value=None)

sector = 'A-U Alle economische activiteiten'
parameter = 'Aantal Banen'
kenmerk = 'Geslacht'
kenmerks = None

f =  open('data/text.txt')
datatext = f.read()

# creating the canvas that contains the filters for the dashboard
offcanvas = html.Div(
    [
        dbc.Button("Filters", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas([
            html.H6('Selecteer Bedrijfstak:', className='canvasheader'), industrydropdown,
            html.H6('Selecteer Parameter:', className='canvasheader'), parameterdropdown,
            html.H6('Selecteer Kenmerk:', className='canvasheader'), catdropdown,
            specdropdown,
            html.Hr(style={'color': 'white'}),
            html.H6('Tips', className='canvasheader'),
            dcc.Markdown(datatext.split('$')[9], id = 'texttip')
            ],
            id="offcanvas",
            title="Filters:",
            is_open=False
        ),
    ]
)

# creating graphs and their divs below. All graphs are created through functions from functions.py.
# Styling through external css file

table = html.Div([functions.create_table()], id='table-div')

catbar = dcc.Graph(figure=functions.make_bars_category(sector, kenmerk, parameter), id='category_bar')
catbarheader = html.H1("Verdeling per Categorie", className='header')
catdiv = html.Div([catbarheader, catbar], id='category-bar-div')

pie = dcc.Graph(figure=functions.create_industry_pie(sector, kenmerks), id='pie_sector')

line = dcc.Graph(figure=functions.create_line(sector, parameter, kenmerk), id='line_sector')
lineheader = html.H1("Ontwikkeling per Jaar", className='header')
linediv = html.Div([lineheader, line], id='line_div')

bars = dcc.Graph(figure=functions.create_bars(parameter, sector, kenmerks), id='bar_industry')
bars_header = html.H6("Verdeling per Bedrijfstak", className='header')
bardiv = html.Div([bars_header, bars], id='industry_bar_div')

container = html.Div([dashboardheader, offcanvas, table, catdiv, pie, linediv, bardiv], id='container')

layout = html.Div(container)


# below are the functions to dynamically update the graphs in the dashboard

@callback(  # opening and closing the canvas
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@callback(  # function to update the industry dropdown through the industry bar.
    Output('industry-picker', 'value'),
    Input('bar_industry', 'clickData'))
def change_sector_picker(clickData):
    sector = 'A-U Alle economische activiteiten'  # declared so when loading app initially it will have correct value
    if clickData is not None:
        string = json.dumps(clickData['points'][0]['hovertemplate']).replace('"', '')
        sector = string[3:string.find('</b>')]
        if sector[0] == 'K':
            sector = 'K Financiële dienstverlening'  # dash doesnt properly read values with special signs.
    return sector

@callback(  # function to update pie
    Output("pie_sector", "figure"),
    [Input('industry-picker', 'value'),
     Input('spec-picker', 'value')])
def change_pie(industry, kenmerks):
    return functions.create_industry_pie(industry, kenmerks)


@callback(  # function to update all figures
    Output('bar_industry', "figure"),
    [Input('industry-picker', 'value'),
     Input('parameter-picker', 'value'),
     Input('spec-picker', 'value')])
def change_industry_bar(industry, parameter, kenmerks):
    return functions.create_bars(parameter, industry, kenmerks)


@callback(  # function to update line and category bar
    Output('line_sector', "figure"),
    Output('category_bar', "figure"),
    [Input('industry-picker', 'value'),
     Input('parameter-picker', 'value'),
     Input('category-picker', 'value')])
def change_category_figures(industry, parameter, category):
    return functions.create_line(industry, parameter, category), functions.make_bars_category(industry, category,
                                                                                              parameter)

@callback(  # spec-pickers values are dependent on category dropdown. function to update options in spec picker
    Output('spec-picker', "options"),
    Output('spec-picker', "value"),
    [Input('category-picker', 'value'),
    Input('category_bar', 'clickData')])
def change_dropdown(category, clickData):
    value = None
    if ctx.triggered_id == 'category_bar':
        value = json.dumps(clickData['points'][0]['label']).replace('"', '')
    labels = worksum[worksum.CategoryGroupID_Kenmerken == catdict[category]]['Kenmerken'].unique()
    speclabels = [{'label': k, 'value': k} for k in labels]
    return speclabels, value


@callback(  # function to highlight selected industry in industry table
    Output("work-table", "style_data_conditional"),
    Input('industry-picker', 'value'))
def change_table(sector):
    return [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#F0F8FF",
        },
        {
            'if': {
                'filter_query': '{Bedrijfstak} eq ' + f'"{sector}"',
            },
            'backgroundColor': '#FFEBCD'
        }
    ]
