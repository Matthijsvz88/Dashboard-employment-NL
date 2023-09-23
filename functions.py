import pandas as pd
import plotly.express as px
from dash.dash_table import DataTable
import numpy as np
from dash import dcc

'''
FUNCTIONS MAIN PAGE

functions That will be used to create the graphs for the mainpage
'''

worksum = pd.read_csv('data/worksum.csv')
description = pd.read_csv('data/description.csv')['Description']
workfull = pd.read_csv('data/workfull.csv')

sector = 'A-U Alle economische activiteiten'
parameter = 'Aantal Banen'
kenmerk = 'Geslacht'
kenmerks = None

# colors for pie chart if no specific industry is selected
colorsa = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52',
           '#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF']

colorss = ['#636EFA' for x in range(0, 19)] #colors for pie if specific industry is selected

#custom labels for pie chart including break lines
labels = ['U Alle economische <br> activiteiten', 'A Landbouw, bosbouw <br> en visserij',
          'B Delfstoffenwinning', 'C Industrie', 'D Energievoorziening',
          'E Waterbedrijven en<br> afvalbeheer', 'F Bouwnijverheid', 'G Handel',
          'H Vervoer en opslag', 'I Horeca', 'J Informatie en<br> communicatie',
          'K Financiële <br>dienstverlening', 'L Verhuur en handel<br> van onroerend goed',
          'M Specialistische <br>zakelijke diensten',
          'N Verhuur en overige<br> zakelijke diensten',
          'O Openbaar bestuur en<br> overheidsdiensten', 'P Onderwijs',
          'Q Gezondheids- en <br> welzijnszorg', 'R Cultuur, sport<br> en recreatie',
          'S Overige <br>dienstverlening']

branchedict = {k: v[2:] for k, v in zip(worksum.Bedrijfstak.unique(), labels)}
catdict = {'Totaal': 1, 'Geslacht': 6, 'Leeftijd': 7, 'Dienstverband': 2, 'Arbeidsduur': 3, 'Bedrijfsomvang': 10,
           'Sector': 11}


def create_industry_pie(industry, kenmerks):
    filterk = 'Totaal'
    if kenmerks is not None: #in case a specific category (men, women) is selected pie chart will show for that category
        filterk = kenmerks
    df = worksum.loc[(worksum.Perioden == 2022) & (worksum.Kenmerken == filterk)].iloc[1:]
    colors = colorsa #regular color scheme in case no industry is selected
    if industry != 'A-U Alle economische activiteiten':
        colors = colorss
    coldict = {k: v for (k, v) in zip(df.sort_values(by='Aantal Banen', ascending=False).Bedrijfstak, colors)} #dict to color selected category red
    pulldict = {v: k for (k, v) in list(enumerate(df.Bedrijfstak))} #dict to pull out selected category from pie
    pull = [0 for x in range(0, 19)]
    if industry != 'A-U Alle economische activiteiten':
        coldict[industry] = '#EF553B'
        pull[pulldict[industry]] = 0.15
    kenmerktitle = f"<br><span style=\"font-size: 14px;\"> ({kenmerks})</span>"  # smaller font for part of title. If specific category is selected will add to pie title
    if kenmerks is None:
        kenmerktitle = ""
    fig = px.pie(df, names=df.Bedrijfstak, values=df['Aantal Banen'], color=df.Bedrijfstak, color_discrete_map=coldict)
    fig.update_layout(
        title={'text': f'<b>{branchedict[industry]}{kenmerktitle}</b>', 'y': 0.94, 'x': 0.5, 'font_size': 20},
        showlegend=False, margin={"t": 75, "l": 5, "r": 5, "b": 10})
    fig.update_traces(pull=pull,textinfo = 'none',
                      hovertemplate="Sector: %{label}: <br>Werknemers: %{value}<br>Procent:%{percent}")
    fig.data[0]['labels'] = labels[1:]
    return fig

# function to create custom hovertext for industry bar chart
def hover_text(x):
    name = x["Bedrijfstak"]
    title = x.index[1]
    param = x[1]
    return (
        f"<b>{name}</b><br>"
        f"{title} - {param}<br>"
    )

#function to create industry barchart at top of the graph
def create_bars(parameter, sector, kenmerks):
    button = [dict(method='restyle', #button for creating comparison bars
                   label='Totaal',
                   visible=True,
                   args=[{'visible': [True, False], }]),
              dict(method='restyle',
                   label='Vergelijking',
                   visible=True,
                   args=[{'visible': [True, True], }])]
    um = [{'buttons': button, 'direction': 'down', 'active': 0, 'x': 0.1, 'y': 1.45}]
    l = ['Aantal Banen', 'Arbeidsvolume'] # used for correct labelling of second bar chart
    filterk = 'Totaal'
    if kenmerks is not None: # if specific category (man, woman) is selected chart will update
        filterk = kenmerks
    df = worksum.loc[(worksum.Perioden == 2022) & (worksum.Kenmerken == filterk)].iloc[1:]
    df = df[['Bedrijfstak', parameter]]
    text = df.apply(hover_text, axis=1) # creating custom text
    colors = colorss.copy()
    kenmerktitle = f'({kenmerks})' #creating subtitle in case specific category is selected.
    if kenmerks is None:
        kenmerktitle = ''
    coldict = {k: v for (k, v) in zip(df.Bedrijfstak, range(0, 19))} #creating color dictionary to color selected industry if one is selected
    if sector != 'A-U Alle economische activiteiten':
        colors[coldict[sector]] = '#EF553B'
    fig = px.bar(df, x='Bedrijfstak', y=parameter)
    fig.update_traces(hovertemplate=text)
    fig.update_layout(title={'text': f'<b>{parameter} {kenmerktitle}</b>', 'y': 0.98, 'x': 0.5},
                      hovermode='x', xaxis={'title': ''}, yaxis={'title': ""}, margin={"t": 33, "l": 5, "r": 5, "b": 0})
    labels = [x[2:14] + '..' if len(x) > 12 else x[2:] for x in fig.data[0]['x']] # shortening the labels to make a better fit on screen
    fig.data[0]['x'] = labels #updating labels in chart
    fig.data[0]['marker']['color'] = colors #updating colors
    # Creating the second bars. Only visible through the chart button
    xy = worksum.loc[(worksum.Perioden == 2022) & (worksum.Kenmerken == 'Totaal')].iloc[1:]
    xy.Bedrijfstak = [x[2:14] + '..' if len(x) > 12 else x[2:] for x in xy.Bedrijfstak]
    fig.add_bar(y=xy[parameter], x=xy.Bedrijfstak, opacity=0.15, width=0.96, offsetgroup=0, hoverinfo='skip',
                name='compare', visible=False)
    fig.update_layout(barmode='overlay', showlegend=False, updatemenus=um)
    partitle = 'Gemiddeld'
    if parameter in l:
        partitle = 'Totaal'
    fig.data[1]['hovertemplate'] = partitle + ': %{y}<extra></extra>'
    return fig

#function to create line chart
def create_line(sector, parameter, kenmerk):
    df = worksum.loc[(worksum.Bedrijfstak == sector) & (worksum.CategoryGroupID_Kenmerken == catdict[kenmerk])]
    fig = px.line(df, x='Perioden', y=parameter, color='Kenmerken')
    fig.update_layout(showlegend=True, legend_font_size=8, hovermode='x unified',
                      margin={"t": 30, "l": 10, "r": 10, "b": 10},
                      legend={'y': -0.15, 'orientation': 'h', 'title': '', 'bgcolor': 'rgba(0,0,0,0)'},
                      xaxis={'title': ''}, yaxis={'title': ''},
                      title={'text': f'<b>{parameter} ({kenmerk})</b>', 'x': 0.5})
    fig.update_traces(hovertemplate=' %{y}')
    return fig

#function to create category bars at bottom left of dashboard
def make_bars_category(sector, kenmerk, parameter):
    category = catdict[kenmerk]
    df = worksum[
        (worksum.Bedrijfstak == sector) & (worksum.Perioden == 2022) & (worksum.CategoryGroupID_Kenmerken == category)]
    fig = px.bar(df, x='Kenmerken', y=parameter)
    fig.update_traces(hovertemplate=' %{y}')
    fig.update_layout(margin={"t": 32, "l": 10, "r": 10, "b": 0}, hovermode='x unified', yaxis={'title': ''},
                      title={'text': f'<b>{parameter} ({kenmerk})</b>', 'x': 0.5}, xaxis={'title': ''})
    return fig

#function to create table at bottom right of dashboard
def create_table():
    df = worksum[(worksum.Perioden == 2022) & (worksum.Kenmerken == 'Totaal')]
    df = df[["Bedrijfstak", "Aantal Banen", 'Arbeidsvolume', 'Gemiddeld uren werk per jaar', 'Uurloon', 'Jaarloon',
             'Description_Branche']]
    # first two columns are text columns, we declare these separately
    columns = [
        {"name": "Bedrijfstak", "id": "Bedrijfstak", "type": "text"}]
    # for other columns we use loop
    for name in df.columns[1:6]:
        col_info = {
            "name": name,
            "id": name,
            "type": "numeric",
            "format": {'specifier': ','}
        }
        columns.append(col_info)
    data = df.to_dict("records")
    work_table = DataTable(
        id="work-table",
        columns=columns,
        data=data,
        fixed_rows={"headers": True},
        tooltip_header={  # create tooltip for headers for small screens. Keeps header content readable
            'Bedrijfstak': {'value': 'Bedrijfstak', 'type': 'markdown'},
            'Aantal Banen': 'Aantal Banen',
            'Arbeidsvolume': 'Arbeidsvolume',
            'Gemiddeld uren werk per jaar': 'Gemiddeld uren werk per jaar',
            'Uurloon': 'Uurloon',
            'Jaarloon':'Jaarloon'
        },
        tooltip_data=[{
            'Bedrijfstak': {'value': row, 'type': 'markdown'}} for row in description],
        css=[{ #css for tooltip
            'selector': '.dash-table-tooltip',
            'rule': 'background-color: #FAF0E6; color: black; font-size: 0.8em; '
                   # 'width:700px !important; max-width:700px !important'
        }],
        tooltip_delay=0, #necessary to make tooltip function properly
        tooltip_duration=None,
        style_table={
            "overflowY": "scroll",
            "borderRadius": "0px 0px 10px 10px",
            "minHeight": "85vh",
            "height": "85vh",
        },
        style_cell={
            "height": "auto",
            "fontFamily": "verdana"
        },
        style_header={  # Styling headers for datatable through CSS
            "textAlign": "center",
            "fontSize": 14,
            "height": "50px",
            "whiteSpace": "normal",
            'backgroundColor': '#2F4F4F',
            "color": "white",
            "font-family": "verdana"
        },
        style_data={  # styling the data within the cell
            "fontSize": 12},

        style_cell_conditional=[  # conditional styling for the cells

            {
                "if": {'column_id': 'Bedrijfstak'},
                'width': '200px',
                "textAlign": "left",
            }
        ],
        style_data_conditional=[  # conditional styling for the data within the cells
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
    )
    return work_table

# function to create dropdown
def create_dropdown(category):
    labels = worksum[worksum.CategoryGroupID_Kenmerken == catdict[category]]['Kenmerken'].unique()
    specdict = dict(zip(labels, labels))
    speclabels = [{'label': k, 'value': k} for k, v in specdict.items()]
    specdropdown = dcc.Dropdown(id='spec-picker', options=speclabels,
                                style={"width": "70%", "textAlign": "center", 'margin-bottom': '10px',
                                       "fontSize": 14, "font-family": "verdana", 'color': 'black'})
    return specdropdown


'''
FUNCTIONS PAGE 2
below functions will be used to create the graphs for page 2 of the employment dashboard

'''
# filters for creating dataframes for functions
mask_bedrijfstak = worksum.Bedrijfstak == 'A-U Alle economische activiteiten'
mask_dienstverband = workfull.Dienstverband == 'Totaal'
mask_voltijd = workfull.Dienstverband == 'Voltijd'
mask_deeltijd = workfull.Dienstverband == 'Deeltijd'
mask_leeftijd = workfull.Leeftijd == 'Totaal'
mask_geslacht = workfull.Geslacht == 'Totaal mannen en vrouwen'
mask_category = workfull.CategoryGroupID == 5
mask_jaar = workfull.Perioden == 2022

#function to create dataframe used in summary table
def create_sum_df():
    df = worksum.loc[(worksum.Kenmerken == 'Totaal') & (worksum.Bedrijfstak == 'A-U Alle economische activiteiten'),
                     ['Perioden', 'Aantal Banen', 'Arbeidsvolume', 'Gemiddeld uren werk per jaar', 'Uurloon',
                      'Jaarloon']]
    df.columns = ['Perioden', 'Aantal Banen (*1000)', 'Arbeidsvolume (*1000)',
                  'Gemiddeld uren werk per jaar', 'Uurloon', 'Jaarloon', ]
    df = pd.melt(df.set_index(['Perioden']), ignore_index=False)
    df['value'] = np.where(df.variable.isin(['Aantal Banen (*1000)', 'Arbeidsvolume (*1000)']), df.value / 1000,
                           df.value)
    df = df.reset_index().pivot(index=['variable'], columns='Perioden', values='value')
    df.reset_index(inplace=True)
    df = df[['variable', 2011, 2016, 2020, 2021, 2022]]
    df.columns = ['Kenmerken', '2011', '2016', '2020', '2021', '2022']
    df['Verschil'] = df['2022'] - df['2011']
    df['Verschil %'] = round((df['2022'] / df['2011'] - 1) * 100, 2)
    return df

#function to create summary table
def summary_table():
    df = create_sum_df()
    columns = [
        {"name": "Kenmerken", "id": "Kenmerken", "type": "text"}
    ]
    for name in df.columns[1:]:
        col_info = {
            "name": name,
            "id": name,
            "type": "numeric",
            "format": {'specifier': ','}
        }
        columns.append(col_info)
    data = df.to_dict("records")
    summary_table = DataTable(
        columns=columns,
        data=data,
        fixed_rows={"headers": True},
        style_table={ #css for table style
            "width": '55vw',
            'max-width': '1400px',
            "overflowY": "scroll",
            'border': '1px black',
            "borderRadius": "0px 0px 10px 10px",
            'marginLeft': 'auto',
            'marginRight': 'auto'
        },
        style_cell={ #styling cells through css
            "height": "auto",
            "fontFamily": "verdana"
        },
        style_header={  # Styling headers for datatable through CSS
            "textAlign": "center",
            "fontSize": 12,
            "height": "50px",
            "whiteSpace": "normal",
        },
        style_data={  # styling the data within the cell
            "fontSize": 12},

        style_cell_conditional=[
            {
                "if": {'column_id': 'Kenmerken'},
                'font-weight': 'bold',
                "textAlign": "left",
            }
        ],
        style_data_conditional=[  # conditional styling for the data within the cells
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fafbfb",
            }
        ]
    )
    return summary_table

#industry bar chart for second page.
def create_bars_industry():
    button = [dict(method='restyle', #button to activate gender comparison
                   label='Totaal',
                   visible=True,
                   args=[{'visible': [False, False, True], }]),
              dict(method='restyle',
                   label='Geslacht',
                   visible=True,
                   args=[{'visible': [True, True, False], }])]

    um = [{'buttons': button, 'direction': 'down', 'active': 0, 'x': 0.13, 'y': 1.2}]
    df = worksum.loc[(worksum.Perioden == 2022) & (worksum.CategoryGroupID_Kenmerken == 6)].iloc[2:]
    df = df[['Kenmerken', 'Bedrijfstak', 'Aantal Banen']]
    fig = px.bar(df, x='Bedrijfstak', y='Aantal Banen', color='Kenmerken')
    fig.update_traces(visible=False)
    fig.update_layout(hovermode='x', margin={"t": 33, "l": 5, "r": 5, "b": 0}, xaxis={'title': ''})
    xy = worksum.loc[(worksum.Perioden == 2022) & (worksum.CategoryGroupID_Kenmerken == 1)].iloc[1:]
    fig.add_bar(x=xy.Bedrijfstak, y=xy['Aantal Banen'], name='Totaal', visible=True)
    fig.update_layout(showlegend=True, updatemenus=um)
    fig.data[2]['hovertemplate'] = '<br>%{x}<br>Aantal Banen :%{y}<extra></extra>'
    return fig

#function to create dataframe for sector development table
def create_sector_df():
    df = worksum[worksum.CategoryGroupID_Kenmerken.isin([1])]
    df = df.pivot(index='Bedrijfstak', columns='Perioden', values='Aantal Banen')
    df.drop(labels='A-U Alle economische activiteiten', inplace=True)
    df = round(df / df.sum() * 100, 2)
    df_sector = df.reset_index()[['Bedrijfstak', 2011, 2016, 2020, 2021, 2022]]
    df_sector.columns = ['Bedrijfstak', '2011', '2016', '2020', '2021', '2022']
    df_sector['verschil'] = df_sector['2022'] - df_sector['2011']
    df_sector.sort_values('verschil', ascending=False, inplace=True)
    return df_sector

#function to create sector development table
def sector_dev_table():
    df = create_sector_df()
    columns = [
        {"name": "Bedrijfstak", "id": "Bedrijfstak", "type": "text"}
    ]
    for name in df.columns[1:]:
        col_info = {
            "name": name,
            "id": name,
            "type": "numeric",
            "format": {'specifier': ','}
        }
        columns.append(col_info)
    data = df.to_dict("records")
    sector_table = DataTable(
        columns=columns,
        data=data,
        fixed_rows={"headers": True},
        style_table={ #table style through css
            "width": '50vw',
            'max-width': '1400px',
            "overflowY": "scroll",
            'border': '1px black',
            "borderRadius": "0px 0px 10px 10px",
            'marginLeft': 'auto',
            'marginRight': 'auto'
        },
        style_cell={ #Cell style through CSS
            "height": "auto",
            "fontFamily": "verdana"
        },
        style_header={  # Styling headers for datatable through CSS
            "textAlign": "center",
            "fontSize": 12,
            "height": "50px",
            "whiteSpace": "normal",
        },
        style_data={  # styling the data within the cell
            "fontSize": 12},

        style_cell_conditional=[
            {
                "if": {'column_id': 'Bedrijfstak'},
                'font-weight': 'bold',
                "textAlign": "left",
            }
        ],
        style_data_conditional=[  # conditional styling for the data within the cells. alternating colors for table
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fafbfb",
            }
        ]
    )
    return sector_table

# function to create company size pie chart
def pie_comp_size():
    df = worksum[
        (worksum.CategoryGroupID_Kenmerken == 10) & (worksum.Bedrijfstak == 'A-U Alle economische activiteiten')]
    pie_comp_size = px.pie(df[(df.Perioden == 2022)], names='Kenmerken', values='Aantal Banen')
    pie_comp_size.update_layout(legend={'x': 0, 'bgcolor': 'rgba(0,0,0,0)'}, legend_font_size=8,
                                margin=dict(t=80, b=20, l=0, r=0), height=300,
                                title={'text': 'Aantal Banen per Bedrijfsomvang', 'x': 0.5})
    return pie_comp_size

#function to create company size line chart
def line_comp_size():
    df = worksum[
        (worksum.CategoryGroupID_Kenmerken == 10) & (worksum.Bedrijfstak == 'A-U Alle economische activiteiten')]
    line_comp_size = px.line(df, x='Perioden', y='Uurloon', color='Kenmerken', height=300)
    line_comp_size.update_layout(hovermode='x unified', title={'text': 'Uurloon per Bedrijfsomvang', 'x': 0.5},
                                 legend_font_size=8,
                                 xaxis={'title': ''},
                                 legend={'y': -0.22, 'orientation': 'h', 'title': '', 'bgcolor': 'rgba(0,0,0,0)'})
    line_comp_size.data[0]['line']['color'] = '#00cc96'
    line_comp_size.data[2]['line']['color'] = '#636efa'
    line_comp_size.data[0]['hovertemplate'] = '0 tot 10 werkzame personen : € %{y}<extra></extra>'
    line_comp_size.data[1]['hovertemplate'] = '10 tot 100 werkzame personen : € %{y}<extra></extra>'
    line_comp_size.data[2]['hovertemplate'] = '100 of meer werkzame personen : € %{y}<extra></extra>'
    return line_comp_size

# fuction to create sector pie chart
def pie_sector():
    df = worksum[
        (worksum.CategoryGroupID_Kenmerken == 11) & (worksum.Bedrijfstak == 'A-U Alle economische activiteiten')]
    pie_sector = px.pie(df[(df.Perioden == 2022)], names='Kenmerken', values='Aantal Banen')
    pie_sector.update_layout(title={'text': 'Aantal Banen per Sector', 'x': 0.5},
                             legend={'x': 0, 'bgcolor': 'rgba(0,0,0,0)'},
                             margin=dict(t=80, b=20, l=0, r=0), legend_font_size=8, height=300)
    return pie_sector

# function to create sector bar chart
def bar_sector():
    df = worksum[
        (worksum.CategoryGroupID_Kenmerken == 11) & (worksum.Bedrijfstak == 'A-U Alle economische activiteiten')]
    bar_sector = px.bar(df[df.Perioden == 2022], x='Kenmerken', y='Uurloon')
    bar_sector.data[0]['marker']['color'] = ['#636efa', '#EF553B', '#00cc96']
    bar_sector.update_layout(title={'text': 'Uurloon per Sector', 'x': 0.5}, xaxis={'title': ''}, height=300,
                             margin_b=0)
    bar_sector.update_xaxes(tickangle=15)
    return bar_sector

#function to create dataframe for gender development table
def df_gender_dev():
    df = worksum[
        (worksum.CategoryGroupID_Kenmerken == 6) & (worksum.Bedrijfstak == 'A-U Alle economische activiteiten')].copy()
    df = df[['Perioden', 'Kenmerken', 'Aantal Banen', 'Arbeidsvolume', 'Gemiddeld uren werk per jaar', 'Uurloon',
             'Jaarloon']]
    df.rename(columns={'Aantal Banen': 'Aantal Banen (*1000)', 'Arbeidsvolume': 'Arbeidsvolume (*1000)',
                       'Kenmerken': 'Sekse'}, inplace=True)
    df = pd.melt(df.set_index(['Perioden', 'Sekse'])[['Aantal Banen (*1000)', 'Arbeidsvolume (*1000)',
                                                      'Gemiddeld uren werk per jaar', 'Uurloon', 'Jaarloon']],
                 ignore_index=False)
    df['value'] = np.where(df.variable.isin(['Aantal Banen (*1000)', 'Arbeidsvolume (*1000)']), df.value / 1000,
                           df.value)
    df = df.reset_index().pivot(index=['variable', 'Sekse'], columns='Perioden', values='value').reset_index()
    df['variable'] = np.where(df.duplicated(subset='variable'), ' ', df.variable)
    df['Ontwikkeling'] = df[2022] - df[2011]
    df.rename(columns={'variable': 'Onderwerp'}, inplace=True)
    df = df[['Onderwerp', 'Sekse', 2011, 2020, 2021, 2022, 'Ontwikkeling']]
    df.columns = ['Onderwerp', 'Sekse', '2011', '2020', '2021', '2022', 'Ontwikkeling']
    return df

#function to create gender development table
def gender_dev_table():
    df = df_gender_dev()
    columns = [
        {"name": "Onderwerp", "id": "Onderwerp", "type": "text"},
        {"name": "Sekse", "id": "Sekse", "type": "text"},
    ]
    # for other columns we use loop
    for name in df.columns[2:]:
        col_info = {
            "name": name,
            "id": name,
            "type": "numeric",
            "format": {'specifier': ','}
        }
        columns.append(col_info)
    data = df.to_dict("records")
    gender_table = DataTable(
        id="gender-table",
        columns=columns,
        data=data,
        fixed_rows={"headers": True},
        style_table={ #Styling table through CSS
            "width": '45vw',
            'max-width': '800px',
            "overflowY": "scroll",
            'border': '1px black',
            "borderRadius": "0px 0px 10px 10px"
        },
        style_cell={ #styling cells through CSS
            "height": "auto",
            "fontFamily": "verdana"
        },
        style_header={  # Styling headers for datatable through CSS
            "textAlign": "center",
            "fontSize": 12,
            "height": "50px",
            "whiteSpace": "normal",
        },
        style_data={  # styling the data within the cell
            "fontSize": 12},

        style_cell_conditional=[ # Styling first two columns through CSS
            {
                "if": {'column_id': 'Onderwerp'},
                'font-weight': 'bold',
                "textAlign": "left",
            },
            {
                "if": {'column_id': 'Sekse'},
                'font-weight': 'bold',
                "textAlign": "left",
            },
        ],
        style_data_conditional=[  # conditional styling for the data within the cells
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fafbfb",
            }
        ]
    )
    return gender_table


# creating dataframe for gender line graph
def gender_line_df():
    df = worksum.loc[mask_bedrijfstak & (worksum.CategoryGroupID_Kenmerken == 6),
                     ['Kenmerken', 'Perioden', "Aantal Banen", 'Arbeidsvolume', 'Gemiddeld uren werk per jaar',
                      'Uurloon', 'Jaarloon']]
    df = pd.melt(df.set_index(['Perioden', 'Kenmerken']), ignore_index=False)
    df = df.set_index('variable', append=True).unstack(1).reset_index()
    df.columns = ['Perioden', 'Onderwerp', 'Mannen', 'Vrouwen']
    df['Verschil'] = round(df['Vrouwen'] / df['Mannen'] * 100, 2)
    df = df.reset_index(drop=True).sort_values(['Perioden', 'Verschil'], ascending=[True, False])
    return df

# function to create line graph
def gender_line_graph():
    df = gender_line_df()
    line_gender = px.line(df, x=df.Perioden, y='Verschil', color='Onderwerp', height=350)
    line_gender.update_layout(hovermode='x unified', title_text='Kenmerken Arbeid vrouw ten opzichte van man',
                              title_x=0.5, xaxis={'title': ''},
                              legend_font_size=8,
                              legend={'y': -0.15, 'orientation': 'h', 'title': '', 'bgcolor': 'rgba(0,0,0,0)'})

    line_gender.data[0]['hovertemplate'] = 'Aantal Banen : %{y}%<extra></extra>'
    line_gender.data[1]['hovertemplate'] = 'Uurloon  : %{y}%<extra></extra>'
    line_gender.data[2]['hovertemplate'] = 'Gemiddeld uren werk  : %{y}%<extra></extra>'
    line_gender.data[3]['hovertemplate'] = 'Arbeidsvolume : %{y}%<extra></extra>'
    line_gender.data[4]['hovertemplate'] = 'Jaarloon  : %{y}%<extra></extra>'
    return line_gender

# function to create gender comparison dataframe for gender table
def gender_industry_df():
    df = worksum[(worksum.Perioden == 2022) & (worksum.CategoryGroupID_Kenmerken == 6)]
    df = df.set_index(['Bedrijfstak', 'Kenmerken']).Uurloon.unstack(-1)
    df['Verschil'] = round(df.Vrouwen / df.Mannen, 2)
    df.sort_values('Verschil', ascending=False, inplace=True)
    df.reset_index(inplace=True)
    return df

# function to create gender industry table
def gender_industry_table():
    df = gender_industry_df()
    columns = [
        {"name": "Bedrijfstak", "id": "Bedrijfstak", "type": "text"},
    ]
    for name in df.columns[1:]:
        col_info = {
            "name": name,
            "id": name,
            "type": "numeric",
            "format": {'specifier': ','}
        }
        columns.append(col_info)
    data = df.to_dict("records")
    gender_pay_table = DataTable(
        id="gender-pay-table",
        columns=columns,
        data=data,
        fixed_rows={"headers": True},
        style_table={ # Styling table through CSS
            "width": '40vw',
            'max-width': '800px',
            "overflowY": "scroll",
            'border': '1px black',
            "borderRadius": "0px 0px 10px 10px",
            'marginLeft': 'auto',
            'marginRight': 'auto'
        },
        style_cell={ #styling cells through CSS
            "height": "auto",
            "fontFamily": "verdana",
            "min-width": "50px"
        },
        style_header={  # Styling headers for datatable through CSS
            "textAlign": "center",
            "fontSize": 12,
            "height": "50px",
            "whiteSpace": "normal",
        },
        style_data={  # styling the data within the cell
            "fontSize": 12},

        style_cell_conditional=[ #styling cells through CSS
            {
                "if": {'column_id': 'Bedrijfstak'},
                'font-weight': 'bold',
                "textAlign": "left",
            }
        ],
        style_data_conditional=[  # conditional styling for the data within the cells
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fafbfb",
            }
        ]
    )
    return gender_pay_table


def gender_contract_age(): #function to create barchart showing hourly rate based on gender, age and contract type
    df_age_gender = workfull[mask_dienstverband & ~mask_leeftijd & ~mask_geslacht & mask_category & mask_jaar]
    df_age_fulltime = workfull[mask_voltijd & ~mask_leeftijd & mask_geslacht & mask_category & mask_jaar]
    df_age_parttime = workfull[mask_deeltijd & ~mask_leeftijd & mask_geslacht & mask_category & mask_jaar]
    button = [dict(method='restyle',
                   label='Sekse',
                   visible=True,
                   args=[{'visible': [True, True, False, False], }]),
              dict(method='restyle',
                   label='Dienstverband',
                   visible=True,
                   args=[{'visible': [False, False, True, True], }])]

    um = [{'buttons': button, 'direction': 'down', 'active': 0, 'x': 0.13, 'y': 1.1}]
    l = ['Aantal Banen', 'Arbeidsvolume']

    fig = px.bar(df_age_gender, x='Leeftijd', y='Gemiddeld Uurloon', color='Geslacht', barmode='group',
                 title='Uurloon Per Leeftijd en Sekse')
    fig.add_bar(x=df_age_fulltime['Leeftijd'], y=df_age_fulltime['Gemiddeld Uurloon'], name='Voltijd', visible=False)
    fig.add_bar(x=df_age_parttime['Leeftijd'], y=df_age_parttime['Gemiddeld Uurloon'], name='Deeltijd', visible=False)
    fig.update_layout(showlegend=True, updatemenus=um, title={'x': 0.5}, margin={'t': 40})
    fig.data[1]['marker']['color'] = '#316395'
    fig.data[3]['marker']['color'] = '#316395'
    return fig


def gender_contract_jobs(): # function to create bar chart showing total jobs by gender and contract type
    df = workfull[~mask_dienstverband & mask_leeftijd & ~mask_geslacht & mask_category & mask_jaar]
    fig = px.bar(df, x='Dienstverband', y='Aantal Banen', color='Geslacht', barmode='group', height=300)
    fig.data[1]['marker']['color'] = '#316395'
    fig.update_layout(margin={'t': 0})
    return fig


def gender_contract_pay(): # function to create bar chart showing hourly pay by gender and contract type
    df = workfull[~mask_dienstverband & mask_leeftijd & ~mask_geslacht & mask_category & mask_jaar]
    fig = px.bar(df, x='Dienstverband', y='Gemiddeld Uurloon', color='Geslacht', barmode='group', height=300)
    fig.data[1]['marker']['color'] = '#316395'
    fig.update_layout(margin={'t': 0})
    return fig
