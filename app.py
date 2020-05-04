import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import mysql.connector
import pandas as pd
import time
import plotly.graph_objects as go


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.title = 'Equity Performance'

def db_connect():
    engine = mysql.connector.connect(
    host="us-cdbr-east-06.cleardb.net",
    user="b299c42f0fdf61",
    passwd="fcdc6acd",
    database="heroku_826bb11c8d537f8"
    )
    return engine
engine = db_connect()
query = """SELECT * FROM equity_history"""
test = pd.read_sql_query(query, engine)
equity_list = test["ticker"].unique().tolist()
print(equity_list)

df = pd.DataFrame()
query = """SELECT DISTINCT ticker FROM equity_history
           WHERE trade_date >= '2019-01-01 12:00:00'"""
answer = pd.read_sql_query(query, engine)

for symb in equity_list:
    query = """select trade_date, close
    from equity_history where ticker='{}' and
    trade_date >= '2019-01-01 12:00:00'
    """.format(symb)
    df2 = pd.read_sql_query(query, engine, index_col='trade_date', parse_dates=['trade_date'])
    df2.rename(columns={"close": symb}, inplace = True)
    df = pd.concat([df, df2], axis=1, join='outer').round(2)
if 'DO' in list(df.columns):
    df['DO'].fillna(0, inplace = True)
df = df.dropna()
Options = []

for symb in equity_list:
    Options.append({'label': symb, 'value': symb})

def run(equity_symb):
    df = pd.DataFrame()
    for symb in equity_symb:
        engine = db_connect()
        query = """select trade_date, close
        from equity_history where ticker='{}' and
        trade_date >= '2019-01-01 12:00:00'
        """.format(symb)
        df2 = pd.read_sql_query(query, engine, index_col='trade_date', parse_dates=['trade_date'])
        df2.rename(columns={"close": symb}, inplace = True)
        df = pd.concat([df, df2], axis=1, join='outer').round(2)
    if 'DO' in list(df.columns):
        df['DO'].fillna(0, inplace = True)
    df = df.dropna()
    return df
min_date = df.index.min()
max_date = df.index.max()
print(min_date, max_date)

def graph_data(column, data_Change):
    num = data_Change[column].iloc[-1]
    if num < 0:
        num = '(' + abs(num).astype(str)+'%)'
    else:
        num = str(num) +'%'
    
    if column == 'PACD':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(0, 152, 214)', width=4, dash='dash'),
                    line_shape='spline',
                    name = column + ' '+ num)
                          
    elif column == 'DO':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(35, 31, 32)', width=3),
                    line_shape='spline',
                    name = column + ' '+ num)
    elif column == 'NE':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(0, 84, 151)', width=3),
                    line_shape='spline',
                    name = column + ' '+ num)
    elif column == 'RIG':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(254, 0, 11)', width=3),
                    line_shape='spline',
                    name = column + ' '+ num)
    elif column == 'SDRL':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(217, 169, 1)', width=3),
                    line_shape='spline',
                    name = column + ' '+ num)
    elif column == 'VAL':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(50, 62, 72)', width=3),
                    line_shape='spline',
                    name = column + ' '+ num)
    elif column == 'Brent':
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(color='rgb(0, 0, 0)', width=3),
                    line_shape='spline',
                    name = column + ' '+ num)
    else:
        
        trace = go.Scatter(x=data_Change.index, y=data_Change[column],
                    mode='lines',
                    text = column,
                    hoverinfo = 'text+x+y',
                    line=dict(width=3),
                    line_shape='spline',
                    name= column + ' '+ num)
    return trace

def annotate(column, data_Change):
    if column == 'PACD':
        text_color = 'rgb(0, 152, 214)'
        
    elif column == 'DO':
        text_color = 'rgb(35, 31, 32)'
        
    elif column == 'NE':
        text_color = 'rgb(0, 84, 151)'

    elif column == 'RIG':
        text_color = 'rgb(254, 0, 11)'
        
    elif column == 'SDRL':
        text_color = 'rgb(217, 169, 1)'
        
    elif column == 'VAL':
        text_color = 'rgb(50, 62, 72)'
    
    elif column == 'Brent':
        text_color = 'rgb(0, 0, 0)'
        
    else:
        text_color = 'rgb(0,0,0)'
        
    num = data_Change[column].iloc[-1]
    if num < 0:
        num = '(' + abs(num).astype(str)+'%)'
    else:
        num = str(num) +'%'
    if column == 'SDRL':
        annotate = dict(
                x = data_Change.index[-1],
                y = data_Change[column].iloc[-1],
                xref="x",
                yref="y",
                text= column + ' ' + num,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor=text_color,
                ax=60,
                ay=0,
                bordercolor=text_color,
                borderwidth=1,
                borderpad=2,
                bgcolor=text_color,
                font=dict(
                    family="Arial",
                    size=14,
                    color= 'rgb(0,0,0)')
                )
    else:
        annotate = dict(
                x = data_Change.index[-1],
                y = data_Change[column].iloc[-1],
                xref="x",
                yref="y",
                text= column + ' ' + num,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor=text_color,
                ax=60,
                ay=0,
                bordercolor=text_color,
                borderwidth=1,
                borderpad=2,
                bgcolor=text_color,
                font=dict(
                    family="Arial",
                    size=14,
                    color= 'rgb(255,255,255)')
                )
    return annotate

def change_line (data, new_line):
    for data in data:
        data['line']['shape'] = new_line

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')

def getMarks(start, end, Nth=31):
    ''' Returns the marks for labeling. 
        Every Nth value will be used.
    '''

    result = {}
    for i, date in enumerate(daterange):
        if(i%Nth == 1):
            # Append value to dict
            result[unixTimeMillis(date)] = str(date.strftime('%b-%Y'))

    return result

daterange = pd.date_range(start=min_date,end=max_date,freq='D')

app.layout = html.Div([

    dbc.Container([

        dbc.Row(
            dbc.Col(
                html.Div(
                    html.Img(src="//s24.q4cdn.com/232570774/files/design/PD-Logo.svg", alt="Pacific Drilling"),
                            id='logo'),
                             width=3,md=3, lg=2),
                             id='head'),

        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H2('Equity Performance')
                ),
                id='title_head')
        ),

        dbc.Row(
            dbc.Col(
                dcc.Graph(id='output',
                config = {'editable' : True, 'toImageButtonOptions': {'format' : 'svg',
                                                                      'height' : 900,
                                                                      'width' : 1500}})
            )
        ),

        dbc.Row(
            dbc.Col(children=[
            dcc.RangeSlider(
                id='my-range-slider',
                min = unixTimeMillis(daterange.min()),
                max = unixTimeMillis(daterange.max()),
                value = [unixTimeMillis(daterange.min()),
                unixTimeMillis(daterange.max())],
                marks=getMarks(daterange.min(),
                                daterange.max())
            ),
        # html.Label('', id='time-range-label'),
        ], id='slider_area')
        ),

        dbc.Row(
            dbc.Col(
                html.Label(
                    html.H6('', id='time-range-label')
            
            ),id='range_label'
            )
        ),

        dbc.Row(
            dbc.Col(
                dbc.FormGroup(
                            [
                    dbc.Label("Toggle Equity Plots"),
                    dbc.Checklist(
                        options=Options,
                        value=equity_list,
                        id="switches-input",
                        switch=True,
                        inline=True,
                                ),
                            ],
                            id='toggle_area'
                )
            )
        ),

    ], fluid=True),
     



])

@app.callback(
    Output('output', 'figure'),
    [Input(component_id='switches-input', component_property='value'),
    Input('my-range-slider', 'value')]
)

def update_value(input_data, date_data):
    df = run(input_data)
    # print(df)
    start_date = unixToDatetime(date_data[0])
    # print(start_date)
    end_date = unixToDatetime(date_data[-1])
    print(end_date)
    df = df[start_date : end_date]
    # print(df)
    data_Change = df.apply(lambda x: ((x-x.iloc[0])/x.iloc[0])*100).round(1)
    traceslist = data_Change.columns.tolist()
    # print(traceslist)
    if 10 + data_Change.min().min() >= -100:
        ax_min = -110
    else:
        ax_min = data_Change.min().min()
        
    if data_Change.max().max() < 20:
        ax_max = 20
        
    else:
        ax_max = data_Change.max().max()+10

    annotations= []
    for i in range(len(traceslist)):
        eachannotate = annotate(traceslist[i], data_Change)
        annotations.append(eachannotate)

    layout = {
        'yaxis': {
            'showgrid': True,
            'gridcolor' : 'rgba(128,128,128, 0.4)',
            'linecolor': 'rgba(128,128,128, 0.4)',
            'zeroline' : True,
            'zerolinecolor' : 'rgb(128,128,128)',
            'ticksuffix' : '%',
            'tickfont' : dict(
                family='Arial',
                size=14,
                color='rgb(82, 82, 82)')
        },
        'xaxis': {
            'showgrid': False,
            'linecolor': 'grey',
            'tickangle' : -45,
            'tickfont' : dict(
                family='Arial',
                size=14,
                color='rgb(82, 82, 82)')
        },
        'plot_bgcolor': 'rgb(255, 255, 255)',
        'showlegend' : False,
        # 'autosize' : False,
        # 'width' : 1800,
        # 'height' : 1000,
        'annotations' : annotations,
        'hovermode' : 'x'
        }
        
    data_graph = []
    # Fill out data with our traces
    for i in range(len(traceslist)):
        eachtrace = graph_data(traceslist[i], data_Change)
        data_graph.append(eachtrace)
    graphs = {'data' : data_graph, 'layout' : layout}

    return graphs
    # return annotations

@app.callback(
    dash.dependencies.Output('time-range-label', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def _update_time_range_label(year_range):
    return 'Showing Equity Return From {} to {}'.format(unixToDatetime(year_range[0]).strftime('%d-%b-%Y'),
                                  unixToDatetime(year_range[1]).strftime('%d-%b-%Y'))



if __name__ == '__main__':
    app.run_server(debug=True)

    html.Img(src="//s24.q4cdn.com/232570774/files/design/PD-Logo.svg", alt="Pacific Drilling")