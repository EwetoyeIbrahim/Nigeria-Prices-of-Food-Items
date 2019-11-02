import sys
import os
# Getting the base directory ensures that my resources are mobile
# especially in this development mode that I am yet to finalize the structure
basedir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir) #When shred resources is within the this folder
sys.path.append(os.path.join(basedir,os.path.pardir))
from _shared_res import public_helpers as public_helpers

import textwrap
#-----------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.tools as tls
#-----------------------------------------------------------
 
external_stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons","https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


states_food_data = pd.read_csv(os.path.join(basedir,'assets','Nigeria States Price of Food Items Jan2016_Aug2019.csv')) # Loading the merged prices
#df.set_index([df.columns[0]],inplace=True)
states_food_prices=states_food_data.copy()
item_list = states_food_prices.ItemLabels.unique()
data_months = list(states_food_prices.columns)[2:]
state_list = ["NIGERIA (Monthly Average)"]
state_list.extend(states_food_prices.States.unique())

#----------------------------------------------------------------
#setting the template variables
with open(os.path.join(basedir,'assets','side_bar.html')) as f:
    sidebar_content = f.read()
    
app.index_string = public_helpers.dashboard_template(page_title='Nigeria Food Prices',
                         page_subtitle='<strong class="green">Visualizing Food Historical Prices</strong>',
                         meta_tag='Nigeria Food Price Trend',
                         header_img_path='./assets/market9.jpg',
                         header_img_alt='Nigeria Food Prices',
                         links_to_related_files = '',
                         generated_advert='',
                         sidebar_content= sidebar_content,
                         list_of_recent_visuals='',
                         )
#-----------------------------------------------------------------

def graph_line_data(state_name, food_name):
    if state_name != "NIGERIA (Monthly Average)":
        state_data = states_food_prices[states_food_prices.States==state_name]
        dat_y = state_data[state_data.ItemLabels==food_name]
        dat_y= dat_y[dat_y.columns[2:]] #The figures part of the frame
    else:
        state_data = states_food_prices.groupby(['ItemLabels']).mean()
        dat_y = state_data[state_data.index==food_name]
    
    return(dat_y)

app.layout = html.Div(
    className="row",
    children=[
        html.Div(#Content without ads
            className="container",
            
            children=[
                html.Div(#The selectors
                    className="row",
                    children=[
                        html.Div(#The state selector
                            className="col-xs-12 col-sm-4",
                            children= [
                                dcc.Dropdown(
                                    id='selected_state',
                                    options=[{'label': i, 'value': i} for i in state_list],
                                    value=['LAGOS'],
                                    multi = True
                                )
                            ],
                        ),
                        html.Div(#The food item selector
                            className="col-xs-12 col-sm-8",
                            children= [
                                dcc.Dropdown(
                                    id='selected_food',
                                    options=[{'label': i, 'value': i} for i in item_list],
                                    value=['Chicken Wings / 1Kg'],
                                    multi = True
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(#The graphs
                    className="row",
                    children = [
                        html.Div(
                            className="col-xs-12 col-sm-7",
                            children=[
                    
                                html.Div(
                                    className="col-xs-12",
                                    children=[dcc.Graph(id='monthly-graph')],
                                    ),
                                
                                html.Div(
                                    className="col-xs-12",
                                    children=[dcc.Graph(id='yoy-graph')],
                                    ),
                                ],
                            ),
                        html.Div(
                            className="col-xs-12 col-sm-5",
                            children=[
                                html.Div(
                                    className="table",
                                    children=[
                                        html.Div(
                                            className="table-responsive",
                                            style={"border-left": "1px solid #eee"},
                                            children=[
                                                dcc.Dropdown(
                                                    id='selected_month',
                                                    options=[{'label': i, 'value': i} for i in data_months],
                                                    value=data_months[-1],
                                                    multi = False,
                                                    style={"margin-top":"5px"}),
                                                dcc.Graph(id='output-table')],
                                        ),]
                                ),],
                            ),
                        
                        html.Div(#The summary section
                            className="col-xs-12", 
                            style={"padding-top":"20px"},
                            children= [
                                dcc.Markdown(id='summary-txt'),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )

@app.callback(
    dash.dependencies.Output('monthly-graph', 'figure'),
    [dash.dependencies.Input('selected_state', 'value'),
     dash.dependencies.Input('selected_food', 'value')])
def update_monthly_graph(selected_state,selected_food):
    traces =[]
    title = "Price trend of "
    if len(selected_food) == 1:
        title = title + selected_food[0]
    else:
        title = title + "foods"
    if len(selected_state) == 1:
         title = title + " in " +selected_state[0]

    for state_name in selected_state:
        for food_name in selected_food:
            graph_data = graph_line_data(state_name, food_name)
            traces.append(
                go.Scatter({
                    'x':graph_data.columns,
                    'y':graph_data.values[0],
                    'mode':'lines',
                    'legendgroup':state_name,
                    'name':f'{state_name} {food_name}',
                    'hovertemplate':'<i>Month</i>: %{x}'
                                    '<br><i>Price</i>: N%{y:.2f}'

                    })
            )
    layout = go.Layout(
        title = {
            'text':title,
            'font':{
                'size':12,
                'color':"#7f7f7f",
            },
        },
            
        legend={
            'orientation':'h',
            'traceorder': 'reversed',
            'x':0.1,
            'y':-0.5,
            'font':{
                'size':10,
            },
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=" Price in Naira (NGN)",
                font=dict(
                    size=12,
                    color="#7f7f7f"
                ),
            ),
        ),
        margin=go.layout.Margin(
            l=5,
            r=0,
            b=0,
            t=50,
            pad=0,
        ),
    )
    fig = {'data':traces, 'layout':layout}
    return go.Figure(fig)

@app.callback(
    dash.dependencies.Output('yoy-graph', 'figure'),
    [dash.dependencies.Input('selected_state', 'value'),
     dash.dependencies.Input('selected_food', 'value')])
def update_yoy_graph(selected_state,selected_food):
    traces =[]
    title = "Year on Year Growth Rate"   

    for state_name in selected_state:
        for food_name in selected_food:
            graph_data = graph_line_data(state_name, food_name) # isolate the needed data
            x=len(graph_data.columns)-1 #number of available months
            
            y=[x-12*i for i in range(round(x/12))] #list of yoy months positions
            yoy_data = [graph_data[graph_data.columns[y]] for x in y ][0].dropna(axis='columns') # lists of yoy data
            yoy_list = yoy_data.values.tolist()[0] # picking up any of the list
            #computing the yoy growth rate list
            yoy_rate = [((yoy_list[io]-yoy_list[io+1])/yoy_list[io])*100 for io in range(len(yoy_list)-1)]
            yoy_rate.append(0) # fixing the last reference value of 0
            yoy_rate.reverse() # reverse the data to cater for chronology
            #print(yoy_rate)
            #print(yoy_data.columns[::-1])
            #print(yoy_data.columns[::-1])
            traces.append(
                go.Scatter({
                    'x':yoy_data.columns[::-1], # chronological order
                    'y':[round(y,2) for y in yoy_rate],
                    'mode':'lines+markers',
                    'hovertemplate':'<i>Month</i>: %{x}'
                                    '<br><i>Growth Rate</i>: %{y:.2f}%<extra></extra>'
                    

                    })
            )
    layout = go.Layout(
        title = {
            'text':title,
            'font':{
                'size':12,
                'color':"#7f7f7f",
            },
        },
        showlegend=False,
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=" Percentage Growth relative to 2016",
                font=dict(
                    size=12,
                    color="#7f7f7f"
                ),
                
            ),
        ),
        margin=go.layout.Margin(
            l=5,
            r=0,
            b=20,
            t=100,
            pad=0,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
    )
    fig = {'data':traces, 'layout':layout}
    return go.Figure(fig)


#-------------------------------------------------------------
# Summary Text callback
#-------------------------------------------------------------

@app.callback(
    dash.dependencies.Output('summary-txt', 'children'),
    [dash.dependencies.Input('selected_state', 'value'),
     dash.dependencies.Input('selected_food', 'value')],)
def summary_txt(selected_state,selected_food):
    summary_txt='#### Brief summary about the trend of '
    if len(selected_food) == 1:
        summary_txt = textwrap.dedent(f'''
                                      {summary_txt} {selected_food[0]}
                                      ---
                                      ''')
    else:
        summary_txt = textwrap.dedent(f'''
                                      {summary_txt} the selected Items
                                      ---
                                      ''')
    for state_name in selected_state:
        for food_name in selected_food:
            graph_data = graph_line_data(state_name, food_name) # isolate the needed data
            x=len(graph_data.columns)-1 #number of available months
            y=[x-12*i for i in range(round(x/12))] #list of yoy months positions
            yoy_data = [graph_data[graph_data.columns[y]] for x in y ][0].dropna(axis='columns') # lists of yoy data
            yoy_list = yoy_data.values.tolist()[0] # picking up any of the list
            if graph_data.values[0][-2] < graph_data.values[0][-1]:
                direction = 'increased'
            if graph_data.values[0][-2] > graph_data.values[0][-1]:
                direction = 'decreased'
            else:
                direction = 'remained constant'
            month_year= graph_data.columns[-1]
            cur_val= yoy_list[-1]
            prev_val= graph_data.values[0][-2]
            year1_price=yoy_list[-2]
            year2_price=yoy_list[-3]
            summary_txt_ = textwrap.dedent(f'''
                                    **In {state_name}, {month_year}:**  
                                    The Average Price of {food_name} {direction} month on month 
                                    to N{cur_val} from N{prev_val} in the previous month. 
                                    By this time last year, the {food_name} was sold at 
                                    N{year1_price} but was sold at N{year2_price} two years ago.
                                    
                                    ''')
            
            summary_txt = summary_txt + summary_txt_
            
    return summary_txt

    
    #To be Used later for table generation
@app.callback(
    dash.dependencies.Output("output-table", "figure"),
    [dash.dependencies.Input('selected_food', 'value'),
        dash.dependencies.Input('selected_month', 'value')],)
def update_table(selected_food,selected_month):
    title = "Prices of "
    if len(selected_food) == 1:
        title = title + selected_food[0]
    else:
        title = title + "foods"
    title = title + " across states"
    value_header = ['State']
    #state_list = ["NIGERIA (Monthly Average)"]
    #value_cell = [df['Name'], df['Team'], df['Position']]
    value_cell = [state_list[1:]] # Eliminating the first option: NIGERIA (Monthly Average)
    for col in selected_food:
        value_header.append(col)
        #select rows with the food_name,reduce to the month columns
        
        value_cell.append(list(states_food_prices[states_food_prices.ItemLabels==col][selected_month].values.round(decimals=2)))
        #print(value_cell)
        #print("len of value_cell = ", len(value_cell))
        #print(value_header)
        #value_cell.append(df[col])
    trace = go.Table(
        header={"values": value_header, "fill": {"color": "grey"}, "align": ['center'],
                "line": {"width": 2, "color": "grey"}, "font": {"size": 10, "color":"white"}},
        cells={"values": value_cell})
    layout = go.Layout(
        title = {
            'text':title,
            'font':{
                'size':12,
                'color':"#7f7f7f",
            },
        },
        height=850,
        margin=go.layout.Margin(
            l=5,
            r=5,
            b=3,
            t=50,
            pad=0,
            ),
        )
    return {"data": [trace], "layout": layout}
    
    
        
if __name__ == '__main__':
    app.run_server(debug=True)
    