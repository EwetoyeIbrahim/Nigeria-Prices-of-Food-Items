import _shared_res.public_helpers as public_helpers
import os
#-----------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.tools as tls
#-----------------------------------------------------------
 
external_stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons"]
external_scripts = ["https://code.jquery.com/jquery-2.1.1.min.js",
                    "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

states_food_data = pd.read_csv(os.getcwd() + '\\states_food_prices.csv') # Loading the merged prices
#df.set_index([df.columns[0]],inplace=True)
states_food_prices=states_food_data.copy()
item_list = states_food_prices.ItemLabels.unique()
state_list = states_food_prices.States.unique()

#----------------------------------------------------------------
#setting the template variables
with open(os.getcwd() + '\\assets\\side_bar.html') as f:
    sidebar_content = f.read()
    
app.index_string = public_helpers.dashboard_template(page_title='Nigeria Food Prices',
                         page_subtitle='<strong class="green">Visualizing Food Historical Prices</strong>',
                         meta_tag='Nigeria Food Price Trend',
                         header_img_path='/assets/market9.jpg',
                         header_img_alt='Nigeria Food Prices',
                         links_to_related_files = '',
                         generated_advert='',
                         sidebar_content= sidebar_content,
                         list_of_recent_visuals='',
                         )
#-----------------------------------------------------------------

def graph_line_data(state_name, food_name):
    if state_name != "NIGERIA":
        state_data = states_food_prices[states_food_prices.States==state_name]
    else:
        state_data = states_food_prices.groupby(['ItemLabels']).mean()
    dat_y = state_data[state_data.ItemLabels==food_name]
    dat_y= dat_y[dat_y.columns[2:]]
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
                            className="col s12 m6 l4",
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
                            className="col s12 m6 l8",
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
                            className="card col s12",
                            children=[dcc.Graph(id='monthly-graph')],
                        ),
                        html.Div(
                            className="card col s12",
                            children=[dcc.Graph(id='yoy-graph')],
                        ),
                    ]
                ),
            ],
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

                    })
            )
    layout = go.Layout(
        title = {
            'text':title,
            'font':{
                'size':14,
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
                    size=14,
                    color="#7f7f7f"
                )
            )
        )
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
            traces.append(
                go.Scatter({
                    'x':yoy_data.columns[::-1], # chronological order
                    'y':yoy_rate,
                    'mode':'lines+markers',
                    

                    })
            )
    layout = go.Layout(
        title = {
            'text':title,
            'font':{
                'size':14,
                'color':"#7f7f7f",
            },
        },
        showlegend=False,
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=" Percentage Growth",
                font=dict(
                    size=14,
                    color="#7f7f7f"
                )
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
    )
    fig = {'data':traces, 'layout':layout}
    return go.Figure(fig)
    
        
if __name__ == '__main__':
    app.run_server(debug=True)
