import dash
from dash import html
import dash_bootstrap_components as dbc
'''
Project update:
add tooltip to column headers
'''
# use pages = True allows to use multiple pages

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

linkgithub = 'https://github.com/Matthijsvz88/Dashboard-employment-NL'
date_header = html.Div(["Gebaseerd op data tot 31-12-2022",html.Br()], id = 'date-header')

# Creating the Navigation bar at the top of dashboard.

nav = dbc.Nav(
    [html.Img(src="assets/logopic.png", id = 'logo-image'),
        dbc.NavLink(["Dashboard Werknemers",html.Br(), "Nederland 2022"], class_name = 'link', href="/"),
        dbc.NavLink(["Analyse Werknemers",html.Br(), "Nederland"], class_name = 'link', href="/analyse"),
        dbc.NavLink(["Check Project",html.Br(),"on GitHub"],target = "_blank",class_name = 'link', href=linkgithub)
    ], id = 'navbar'
)

layout = html.Div(
    [nav,date_header, dash.page_container # dash.page_container contains the page data you find in pages file
     ])

app.layout = layout

if __name__ == "__main__":
    app.run(debug=False, port=8011)