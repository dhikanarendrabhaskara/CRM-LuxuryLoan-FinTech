import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
from dash.dependencies import Input, Output, State
import pickle
import dash_table

def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size)

data = pd.read_csv('LuxuryLoanEdit.csv')
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('LUXURY LOAN PORTFOLIO'),
    html.Div(children='by Dhika Narendra Bhaskara'),

    dcc.Tabs(children=[
        dcc.Tab(value='Tab1', label='DataFrames',children=[
            html.Div([
                html.Div(children=[
                    html.P('Purpose: '),
                    dcc.Dropdown(id='filter-purpose', value = 'None',
                    options= [{'label' : 'None', 'value' : 'None'},
                              {'label' : 'Home', 'value' : 'home'},
                              {'label' : 'Boat', 'value' : 'boat'},
                              {'label' : 'Plane', 'value' : 'plane'},
                              {'label' : 'Investment Property', 'value' : 'investment property'},
                              {'label' : 'Commercial Property', 'value' : 'commercial property'},
                              ])
                ], className='col-3'),

                html.Div(children=[
                    html.P('Duration: '),
                    dcc.Dropdown(id='filter-duration', value = 'None',
                    options= [{'label' : 'None', 'value' : 'None'},
                              {'label' : '10 years', 'value' : 10},
                              {'label' : '15 years', 'value' : 15},
                              {'label' : '20 years', 'value' : 20},
                              {'label' : '30 years', 'value' : 30},
                              ]),
                ], className='col-3'),
            ], className='row'),
            
            html.Br(),
            html.Div([
                html.P('Max Rows: '),
                dcc.Input(id ='filter-row',
                            type = 'number', 
                            value = 10)
                ], className = 'row col-3'),
            
            html.Div(children=[
                html.Button('search', id = 'filter')
                ],className = 'row col-4'),
            
            html.Br(),                
            html.Div(id='div-table',
                children=[generate_table(data)])
        ]),

        dcc.Tab(value='Tab2', label='Plots & Graphs',children=[
            html.Div([dcc.Graph(
                id='Graph1',
                figure ={
                'data':[
                    {'x': data['purpose'],'y': data['funded_amount'], 'type': 'violin', 'name':'violinplot' },
                    {'x': data['duration years'],'y': data['funded_amount'], 'type': 'box', 'name':'boxplot' }   
                ],
                'layout': {'title': 'Loan Purpose, Duration-Years & Amount'}
            })
            ], className = 'col-12'),

            html.Div([
                html.Div(children = dcc.Graph(
                    id = 'Graph2',
                    figure = {'data':[
                    go.Pie(
                        labels = data['purpose'].unique(),
                        values = [data[data['purpose']=='home']['funded_amount'].mean(),
                                data[data['purpose']=='boat']['funded_amount'].mean(),
                                data[data['purpose']=='plane']['funded_amount'].mean(),
                                data[data['purpose']=='investment property']['funded_amount'].mean(),
                                data[data['purpose']=='commercial property']['funded_amount'].mean()], 
                                textinfo='percent')            
                    ],
                    'layout': go.Layout(title='Loan Purpose & Amount Average', hovermode = 'closest')
                }
                ), className = 'col-6'),

                html.Div(children = dcc.Graph(
                    id = 'Graph22',
                    figure = {'data':[
                    go.Pie(
                        labels = data['duration years'].unique(),
                        values = [data[data['duration years']== 30]['funded_amount'].mean(),
                                data[data['duration years']== 20]['funded_amount'].mean(),
                                data[data['duration years']== 15]['funded_amount'].mean(),
                                data[data['duration years']== 10]['funded_amount'].mean()], 
                                textinfo='percent')           
                    ],
                    'layout': go.Layout(title='Duration Years & Amount Average', hovermode = 'closest')
                }
                ), className = 'col-6'),
            ], className='row'),
  
            html.Div(children = dcc.Graph(
                id = 'Graph3',
                figure = {'data':[
                go.Scatter(
                    x=data[data['purpose']==i]['interest rate percent'],
                    y=data[data['purpose']==i]['funded_amount'],
                    mode='markers',
                    name='{}'.format(i)
                    ) for i in data['purpose'].unique()            
                ],
                'layout':go.Layout(
                    xaxis={'title':'Interest Rate'},
                    yaxis={'title':'Loan Amount'},
                    title='Loan Amount & Interest Rate',
                    hovermode='closest'
                )
            }   
            ), className = 'col-11'), 
        ])#dcc.Tab       

    ], content_style= {
            'fontFamily': 'Arial',
            'borderBottom': '1px solid #d6d6d6',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'padding': '44px'
        }
    )#dcc.Tabs 
    ]#children(app_layout)
)#app_layout

@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'),
    State(component_id = 'filter-purpose', component_property = 'value'),
    State(component_id = 'filter-duration', component_property = 'value')]
)

def update_table(n_clicks, row, purpose, duration):
    data = pd.read_csv('LuxuryLoanEdit.csv')
    if purpose != 'None':
        data = data[data['purpose'] == purpose]
    if duration != 'None':
        data = data[data['duration years'] == duration]
    children = [generate_table(data, page_size = row)]
    return children
      
if __name__ == '__main__':
    app.run_server(debug=True)