import dash_bootstrap_components as dbc
from dash import html
import dash
from dash import dcc
import functions

dash.register_page(__name__, path='/analyse', name='Analyse Werknemers Nederland') # registering the page to connect to main page

link = 'https://opendata.cbs.nl/portal.html?_la=nl&_catalog=CBS&tableId=81434ned&_theme=6'
source = html.Div(["bron: ", dcc.Link('CBS Open Data Statline', href=link, target="_blank")], id='source-link', style={'grid-area': 'header'})

f =  open('data/text.txt')
datatext = f.read()

text_summary = dcc.Markdown(datatext.split('$')[0],className = 'textbox')
summary_table_div = html.Div([dbc.Row([functions.summary_table()])])

summary_div = html.Div([text_summary, summary_table_div])

text_markets = dcc.Markdown(datatext.split('$')[1],className = 'textbox')
bars_graph = dcc.Graph(figure = functions.create_bars_industry(), id = 'industry-bars-2')
text_dev = dcc.Markdown(datatext.split('$')[2],className = 'textbox')
industry_table_div = html.Div(functions.sector_dev_table())

industry_div = html.Div([text_markets, bars_graph, text_dev, industry_table_div])

text_size = dcc.Markdown(datatext.split('$')[3],className = 'textbox')

pie_size_graph = dcc.Graph(figure = functions.pie_comp_size())
line_size_graph = dcc.Graph(figure = functions.line_comp_size())

row_content_size = [
    dbc.Col(pie_size_graph, width = 5),
    dbc.Col(line_size_graph,width = 6),
]

comp_size_div = html.Div([dbc.Row(row_content_size, justify="center")])

size_div = html.Div([text_size,comp_size_div])

text_sector = dcc.Markdown(datatext.split('$')[4],className = 'textbox')

bar_sector_graph = dcc.Graph(figure = functions.bar_sector())
pie_sector_graph = dcc.Graph(figure = functions.pie_sector())

row_content_sector = [
    dbc.Col(pie_sector_graph, width = 5),
    dbc.Col(bar_sector_graph,width = 6),
]

comp_sector_div = html.Div([dbc.Row(row_content_sector, justify="center")])

sector_div = html.Div([text_sector, comp_sector_div])

text_gender_1 = dcc.Markdown(datatext.split('$')[5],className = 'textbox')


table_div = html.Div([functions.gender_dev_table()])
line_div = dcc.Graph(figure = functions.gender_line_graph())

row_content_gender = [
    dbc.Col(table_div, width = 5),
    dbc.Col(line_div,width = 6),
]

gender_dev = dbc.Row(row_content_gender, justify="between", style = {'padding-left':'25px'})

text_gender_2 = dcc.Markdown(datatext.split('$')[6],className = 'textbox')

gender_pay_div = html.Div([functions.gender_industry_table()])

text_gender_3 = dcc.Markdown(datatext.split('$')[7],className = 'textbox')

gender_age_graph = dcc.Graph(figure = functions.gender_contract_age(), id = 'gender-age-graph')

text_gender_4 = dcc.Markdown(datatext.split('$')[8],className = 'textbox')

work_gen_graph = dcc.Graph(figure = functions.gender_contract_jobs())
pay_gen_graph = dcc.Graph(figure = functions.gender_contract_pay())

row_content_gen = [
    dbc.Col(work_gen_graph, width = 6),
    dbc.Col(pay_gen_graph,width = 6),
]

gender_pay_work = dbc.Row(row_content_gen, justify="center", style = {'padding-left':'25px'})

gender_div = html.Div([text_gender_1, gender_dev, text_gender_2,gender_pay_div,text_gender_3,gender_age_graph,
                       text_gender_4, gender_pay_work])

layout = html.Div([source, summary_div,industry_div, gender_div,size_div, sector_div], id = 'layout-analysis',style = {'max-width':'2000px','margin':'auto'})
