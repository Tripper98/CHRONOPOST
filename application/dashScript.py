###############################################################################
#                                MAIN                                         #
###############################################################################

# Setup
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from settings import config, about
from python.process import Process
from python.data import Data
from python.charts import Chart
# from python.model import Model



data = Data()
data.get_data()

# App Instance
app = dash.Dash(name=config.name, assets_folder=config.root+"/application/static", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name


# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    #dbc.NavItem(html.Img(src=app.get_asset_url("dralyze.png"), height="70px")),
    ## about
    dbc.NavItem(html.Div([
        dbc.NavLink("About", href="/", id="about-popover", active=False),
        dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            dbc.PopoverHeader("How it works"), dbc.PopoverBody(about.txt)
        ])
    ])),
    ## links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-linkedin"), "  Contacts"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank")
    ])
])

# Input
inputs = dbc.FormGroup([
    html.H4("Select Dataframe"),
    dcc.Dropdown(id="dataframe", options=[{"label":x,"value":x} for x in data.li], value="shipments")
])


map_input = dbc.FormGroup([
    html.H4("Select a Feature"),
    dcc.Dropdown(id="map_feature", options=[{"label":x,"value":x} for x in data.get_columns_map()], value="TOTAL PRICE")
])

# products input 
products_input = dbc.FormGroup([
    dcc.Dropdown(id="product_name", options=[{"label":x,"value":x} for x in data.get_product_customer().PROD_NAME.unique().tolist()],placeholder="Select a Product") 
])

plots_top_top = html.Div([
    dbc.FormGroup([
    dcc.Dropdown(id="top_top", options=[{"label":x,"value":x} for x in data.get_columns_map()],placeholder="Top Customers By")
    ])
    ])

plots_worst_worst = html.Div([
    dbc.FormGroup([
    dcc.Dropdown(id="worst_worst", options=[{"label":x,"value":x} for x in data.get_columns_map()],placeholder="Worst Customers By")
    ])
    ])

time_series_products = html.Div([
    dbc.FormGroup([
    dcc.Dropdown(id="analyze_by", options=[{"label":x,"value":x} for x in data.get_columns_map()],placeholder="Analyze By")
    ])
    ])

# Map panel a jmmi 
recevers = data.get_map_data() 
senders = data.get_map_data_sender() 
inactive = 195-max(senders.shape[0],recevers.shape[0])       
map_panel = html.Div(
            dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("Active Senders countries:", style={"color":"white"}),
            html.H3("{:,.0f}".format(senders.shape[0]), style={"color":"white"}),
            
            html.H6("Active Recevers countries:", style={"color":"white"}),
            html.H3("{:,.0f}".format(recevers.shape[0]), style={"color":"white"}),
            
            html.H6("Inactive Countries:", className="text-danger"),
            html.H3("{:,.0f}".format(inactive), className="text-danger")
        ])
        )

# App Layout
app.layout = dbc.Container(fluid=True, children=[
    ## Top
    #html.H1(config.name, id="nav-pills"),
    html.Img(src=app.get_asset_url("dralyze.png"),height="100px"),
    navbar,
    html.Br(),html.Br(),

    ## Body
    dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            map_input,
            html.Br(),html.Br(),
            map_panel
        ]),
        ### plots
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("Map Analysing"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="map-plot"), label="Receiver Country")
            
            ])
        ])
        
                
    ]),

    dbc.Row(
            [   
                
                dbc.Col(md=3, children=[
                   # html.Div(id="cluster-panel")
            ]),

                dbc.Col(md=9, children=[
                #html.Div(id="cluster-title"),
                dbc.Tabs(className="nav nav-pills", children=[
                 dbc.Tab(dcc.Graph(id="map-plot-sender"), label="Sender Country")
                
            ])
                        ])
            ]
        ),

    dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            inputs,
            html.Div(id="name_group"),
            html.Div(id="city_type")
        ]),
        ### plots
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("ML Analysis"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="k-means"), label="K-means Clustering")
                # dbc.Tab(dcc.Graph(id="horizontal-bar"), label="K-means insight")
                
            ])
        ])
        
                
    ]),
        dbc.Row(
            [   
                dbc.Col(md=3, children=[
                    
            ]),

                dbc.Col(md=9, children=[
                        dbc.Col(html.H4("General Info about clusters"), width={"size":6,"offset":3}), 
                         dbc.Tabs(className="nav nav-pills", children=[
                            dbc.Tab(dcc.Graph(id="horizontal-bar"), label="K-means Insight"),
                            dbc.Tab(dcc.Graph(id="...."), label="....")
                
            ])
        ])
            ]
        ),

        dbc.Row(
            [   
                
                dbc.Col(md=3, children=[
                    html.Div(id="cluster-panel-output"),
                    html.Br(),
                    html.Div(id="cluster-insight"),
                    html.Br()
                    #html.Div(id="customers-insight")
                    
            ]),

                dbc.Col(md=9, children=[

                html.Div(id="cluster-title"),
                html.Div(id="customer-dropdown"),
                dcc.Graph(id="pie-chart"),


                   
            ])
                    ]),

       
        dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
           products_input
        ]),
        ### plots
        dbc.Col(md=9, children=[
                
                time_series_products,
                dcc.Graph(id="time_products"),

                plots_top_top,
                dcc.Graph(id="top-plots"),

                plots_worst_worst,
                dcc.Graph(id="worst-plots")
            
        ])
        
                
    ]),

    dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            
        ]),
        ### plots
        dbc.Col(md=9, children=[
            
                
        ])
        
                
    ])

])

# Select the city or type of clients 
@app.callback(output=Output("name_group","children"), inputs=[Input("dataframe","value")])
def render_output_column(dd):

    data = Data()
    bool_val = True
    if dd == 'big_df' :
        bool_val = False

    panel = html.Div([
    dbc.FormGroup([
    dcc.Dropdown(id="name_group_id", options=[{"label":x,"value":x} for x in data.get_names_groupe()], value = "City", disabled = bool_val)
    ])
    ])
  
    return panel

# Select the city or type of clients 
@app.callback(output=Output("city_type","children"), inputs=[Input("name_group_id","value"),Input("dataframe","value")])
def render_output_city(name,dd):

    bool_val = True
    if dd == 'big_df' :
        bool_val = False
    data = Data()
    var = "Casablanca"
    if name == "Type Of Customer" : 
        li = data.get_types()
        var = 'A'
    else : 
        li = data.get_cities()
    panel = html.Div([
    dbc.FormGroup([
    dcc.Dropdown(id="drop_city_type", options=[{"label":x,"value":x} for x in li], value = var, disabled= bool_val )
    ])
    ])
  
    return panel



# Time Series/ Products plot
@app.callback(output=Output("time_products","figure"), inputs=[Input("product_name","value"),Input("analyze_by","value")])
def render_cluster_plots_products(name,filtre):
    data = Data()
    df = data.get_product_data(name)
    chart = Chart()
    return chart.plot_time_series(df,filtre)



#Python function to plot pie chart
@app.callback(output=Output("pie-chart","figure"), inputs=[Input("customers","value")]) 
def plot_pie(customer):
    data = Data()
    df = data.get_product_customer().groupby('CUST_NAME')
    df_cust = df.get_group(customer) 
    chart = Chart()
    return chart.plot_pie(df_cust,customer)


#Python function to plot cluster panel 
@app.callback(output=Output("cluster-insight","children"), inputs=[Input("cluster-panel","value"),Input("dataframe","value"),Input("customers","value"),Input("name_group_id","value"),Input("drop_city_type","value")])
def render_cluster_title(cluster_panel,dataframe,customer,in1,in2):
    if dataframe == "shipments" : 
        d= data.get_shp_cluster_name(cluster_panel,dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        x_df = all_df[1]
        kk = x_df.groupby('cluster')
        d = kk.get_group(int(cluster_panel))
        
    info = data.get_info(d)
    info_customer = data.get_info_cust(dataframe,customer)
    print('####################')
    print(info)
    panel = html.Div([
        html.H4('Cluster {}'.format(cluster_panel)),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("mean || Total Price:", style={"color":"white"}),
            html.H3("{:,.0f}".format(info[1]), style={"color":"white"}),
            
            html.H6("mean || Total Shipments:", className="text-danger"),
            html.H3("{:,.0f}".format(info[0]), className="text-danger"),
        ]),
        html.Br(),html.Br(),

        html.H4('{}'.format(customer)),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("Total Price:", style={"color":"white"}),
            html.H3("{:,.0f}".format(info_customer[0]), style={"color":"white"}),
            
            html.H6("Total Shipments:",  style={"color":"white"}),
            html.H3("{:,.0f}".format(info_customer[1]), style={"color":"white"}),
        ])
    ])
    return panel

#Python function to plot customer panel 
# @app.callback(output=Output("customers-insight","children"), inputs=[Input("customers","value"),Input("dataframe","value")])
# def render_customers_panel(customer,dataframe):
#     info = data.get_shp_customer_info(customer,dataframe)
#     print(info[0])
#     panel = html.Div([
#         html.H4('{}'.format(customer)),
#         dbc.Card(body=True, className="text-white bg-primary", children=[
            
#             html.H6("Total Price:", style={"color":"white"}),
#             html.H3("{:,.0f}".format(info[1]), style={"color":"white"}),
            
#             html.H6("Total Shipments:", className="text-danger"),
#             html.H3("{:,.0f}".format(info[0]), className="text-danger"),
#         ])
#     ])
#     return panel

# map plot 
@app.callback(output=Output("map-plot","figure"), inputs=[Input("map_feature","value")]) 
def plot_map(map_feature):
    df = data.get_map_data()   
    chart = Chart()
    return chart.plot_map(df,map_feature)

@app.callback(output=Output("map-plot-sender","figure"), inputs=[Input("map_feature","value")]) 
def plot_map(map_feature):
    df = data.get_map_data_sender()   
    chart = Chart()
    return chart.plot_map(df,map_feature)



# Top plots 
@app.callback(output=Output("top-plots","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value"),Input("top_top","value"),Input("name_group_id","value"),Input("drop_city_type","value")])
def render_cluster_plots(cluster_panel,dataframe,top_top,in1,in2):
    if dataframe == "shipments" : 
       d = data.get_shp_cluster_name(cluster_panel,dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        df = all_df[1]
        kk = df.groupby('cluster')
        d = kk.get_group(int(cluster_panel))
    
    if top_top == "TOTAL KG": 
        details = data.get_top_kgs(d)
        chart = Chart()
        return chart.plot_h_top(details,True)
    elif top_top == "TOTAL VOLUME":
        details = data.get_top_volume(d)
        chart = Chart()
        return chart.plot_h_top(details,True)
    elif top_top == "TOTAL PRICE":
        details = data.get_top_price(d)
        chart = Chart()
        return chart.plot_h_top(details,True)
    else : 
        details = data.get_top_shps(d)
        chart = Chart()
        return chart.plot_h_top(details,True)


## Worst plots 
@app.callback(output=Output("worst-plots","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value"),Input("worst_worst","value"),Input("name_group_id","value"),Input("drop_city_type","value")])
def render_cluster_plots_worst(cluster_panel,dataframe,worst_worst,in1,in2):
    if dataframe == "shipments" : 
       d = data.get_shp_cluster_name(cluster_panel,dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        df = all_df[1]
        kk = df.groupby('cluster')
        d = kk.get_group(int(cluster_panel))
    if worst_worst == "TOTAL KG": 
        details = data.get_buttom_kgs(d)
        chart = Chart()
        return chart.plot_h_top(details,False)
    elif worst_worst == "TOTAL VOLUME":
        details = data.get_buttom_volume(d)
        chart = Chart()
        return chart.plot_h_top(details,False)
    elif worst_worst == "TOTAL PRICE":
        details = data.get_buttom_price(d)
        chart = Chart()
        return chart.plot_h_top(details,False)
    else : 
        details = data.get_buttom_shps(d)
        chart = Chart()
        return chart.plot_h_top(details,False)

# Plot scatter
@app.callback(output=Output("k-means","figure"), inputs=[Input("dataframe","value"),Input("name_group_id","value"),Input("drop_city_type","value")]) 
def plot_k_means(dataframe,in1,in2):
    if dataframe == "shipments" : 
        pca_df = data.get_pca(dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        pca_df = all_df[0]

    chart = Chart()
    return chart.plot_scatter(pca_df)


# Plot cluster's general insights 
@app.callback(output=Output("horizontal-bar","figure"), inputs=[Input("dataframe","value"),Input("name_group_id","value"),Input("drop_city_type","value")]) 
def plot_h_cluster(dataframe,in1,in2):
    if dataframe == "shipments" : 
        pca_df = data.get_pca(dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        pca_df = all_df[0]
    chart = Chart()
    return chart.plot_h_bar(pca_df)

#dropdown cluster 
@app.callback(output=Output("cluster-panel-output","children"), inputs=[Input("dataframe","value"),Input("name_group_id","value"),Input("drop_city_type","value")])
def render_output_panel(dataframe,in1,in2):
    if dataframe == "shipments" : 
        x_df = data.get_pca(dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        x_df = all_df[0]
    
    clusters = x_df.cluster.unique().tolist()
    
    panel = html.Div([
    dbc.FormGroup([
    html.H4("Select Cluster"),
    dcc.Dropdown(id="cluster-panel", options=[{"label":x,"value":x} for x in clusters], value="0")
    ])
    ])
    return panel

#customers clustering 
@app.callback(output=Output("customer-dropdown","children"), inputs=[Input("cluster-panel","value"),Input("dataframe","value"),Input("name_group_id","value"),Input("drop_city_type","value")])
def render_output_customer(panel,dataframe,in1,in2):
    if dataframe == "shipments" : 
        x_df= data.get_shp_cluster_name(panel,dataframe)
    else : 
        kmeans = Process()
        all_df = kmeans.K_means(in1,in2)
        df = all_df[1]
        kk = df.groupby('cluster')
        x_df = kk.get_group(int(panel))
    names = x_df.CUST_NAME.tolist()
    panel = html.Div([
    dbc.FormGroup([
    dcc.Dropdown(id="customers", options=[{"label":x,"value":x} for x in names],value= "MTCM")
    ])
    ])
    return panel

#cluster title
@app.callback(output=Output("cluster-title","children"), inputs=[Input("cluster-panel","value")])
def render_cluster_title(cluster_panel):
    panel = html.Div([ dbc.Col(html.H4('Insights About Cluster {}'.format(cluster_panel)), width={"size":6,"offset":3})
            ])
    return panel





'''
# Read data
data = Data()
data.get_data()



# App Instance
app = dash.Dash(name=config.name, assets_folder=config.root+"/application/static", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name

# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    ## logo/home
    dbc.NavItem(html.Img(src=app.get_asset_url("chronopost.png"), height="40px")),
    ## about
    dbc.NavItem(html.Div([
        dbc.NavLink("About", href="/", id="about-popover", active=False),
        dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            dbc.PopoverHeader("How it works"), dbc.PopoverBody(about.txt)
        ])
    ])),
    ## links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-linkedin"), "  Contacts"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank")
    ])
])



# Input
inputs = dbc.FormGroup([
    html.H4("Select Country"),
    dcc.Dropdown(id="country", options=[{"label":x,"value":x} for x in data.countrylist], value="World")
]) 



# App Layout
app.layout = dbc.Container(fluid=True, children=[
    ## Top
    html.H1(config.name, id="nav-pills"),
    navbar,
    html.Br(),html.Br(),html.Br(),

    ## Body
    dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            inputs, 
            html.Br(),html.Br(),html.Br(),
            html.Div(id="output-panel")
        ]),
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("Forecast 30 days from today"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="plot-total"), label="Total cases"),
                dbc.Tab(dcc.Graph(id="plot-active"), label="Active cases")
            ])
        ])
    ]),
    dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"),md=6),
                dbc.Col(html.Div("One of three columns"),md=2),
                dbc.Col(html.Div("One of three columns"),md=2),
            ]
        )
])



# Python functions for about navitem-popover
@app.callback(output=Output("about","is_open"), inputs=[Input("about-popover","n_clicks")], state=[State("about","is_open")])
def about_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(output=Output("about-popover","active"), inputs=[Input("about-popover","n_clicks")], state=[State("about-popover","active")])
def about_active(n, active):
    if n:
        return not active
    return active



# Python function to plot total cases
@app.callback(output=Output("plot-total","figure"), inputs=[Input("country","value")]) 
def plot_total_cases(country):
    data.process_data(country) 
    model = Model(data.dtf)
    model.forecast()
    model.add_deaths(data.mortality)
    result = Result(model.dtf)
    return result.plot_total(model.today)



# Python function to plot active cases
@app.callback(output=Output("plot-active","figure"), inputs=[Input("country","value")])
def plot_active_cases(country):
    data.process_data(country) 
    model = Model(data.dtf)
    model.forecast()
    model.add_deaths(data.mortality)
    result = Result(model.dtf)
    return result.plot_active(model.today)
    

    
# Python function to render output panel
@app.callback(output=Output("output-panel","children"), inputs=[Input("country","value")])
def render_output_panel(country):
    data.process_data(country) 
    model = Model(data.dtf)
    model.forecast()
    model.add_deaths(data.mortality)
    result = Result(model.dtf)
    peak_day, num_max, total_cases_until_today, total_cases_in_30days, active_cases_today, active_cases_in_30days = result.get_panel()
    peak_color = "white" if model.today > peak_day else "red"
    panel = html.Div([
        html.H4(country),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("Total cases until today:", style={"color":"white"}),
            html.H3("{:,.0f}".format(total_cases_until_today), style={"color":"white"}),
            
            html.H6("Total cases in 30 days:", className="text-danger"),
            html.H3("{:,.0f}".format(total_cases_in_30days), className="text-danger"),
            
            html.H6("Active cases today:", style={"color":"white"}),
            html.H3("{:,.0f}".format(active_cases_today), style={"color":"white"}),
            
            html.H6("Active cases in 30 days:", className="text-danger"),
            html.H3("{:,.0f}".format(active_cases_in_30days), className="text-danger"),
            
            html.H6("Peak day:", style={"color":peak_color}),
            html.H3(peak_day.strftime("%Y-%m-%d"), style={"color":peak_color}),
            html.H6("with {:,.0f} cases".format(num_max), style={"color":peak_color})
        
        ])
    ])
    return panel

'''