def bake_mars():
    filterk = 'Totaal'
    df = worksum.loc[(worksum.Perioden == 2022)&(worksum.CategoryGroupID_Kenmerken == 6)].iloc[2:]
    df = df[['Kenmerken','Bedrijfstak','Aantal Banen']]
    fig = px.bar(df, x = 'Bedrijfstak', y = 'Aantal Banen', color = 'Kenmerken')
    fig.update_traces(visible = False)
    fig.update_layout( hovermode = 'x', margin={"t": 33, "l": 5, "r": 5, "b": 0}, xaxis = {'title':''})
    xy = worksum.loc[(worksum.Perioden == 2022)&(worksum.CategoryGroupID_Kenmerken == 1)].iloc[1:]
    fig.add_bar(x = xy.Bedrijfstak,y = xy['Aantal Banen'], name = 'Totaal', visible = True)
    fig.update_layout(showlegend = True, updatemenus=um)
    fig.data[2]['hovertemplate'] = '<br>%{x}<br>Aantal Banen :%{y}<extra></extra>'
    return fig