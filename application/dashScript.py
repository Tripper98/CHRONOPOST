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

customer_input = dbc.FormGroup([
    html.H4("To DO "),
    dcc.Dropdown(id="cust_id", options=[{"label":x,"value":x} for x in data.li], value="")
])

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
            map_input
        ]),
        ### plots
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("Map Analysing"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="map-plot"), label="Receiver Country"),
                dbc.Tab(dcc.Graph(id="map-plot-sender"), label="Sender Country")
               
                
            ])
        ])
        
                
    ])
    ,dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
            inputs
        ]),
        ### plots
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("ML Analysis"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="k-means"), label="K-means Clustering"),
                dbc.Tab(dcc.Graph(id="plot-active"), label="Hierarchical Clustering")
                
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
                    html.Div(id="cluster-panel"),
                    html.Br(),html.Br(),
                    html.Div(id="cluster-insight")
            ]),

                dbc.Col(md=9, children=[
                html.Div(id="cluster-title"),
                dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="top-plot"), label="Top customers / Total kgs"),
                dbc.Tab(dcc.Graph(id="top-plot-kgs"), label="Top customers / Total shipment"),
                dbc.Tab(dcc.Graph(id="top-plot-volume"), label="Top customers / Total volume"),
                dbc.Tab(dcc.Graph(id="top-plot-price"), label="Top customers / Total price"),
                dbc.Tab(dcc.Graph(id="..."), label="...")
                
            ])
                        ])
            ]
        ),

        dbc.Row(
            [   
                
                dbc.Col(md=3, children=[
                   # html.Div(id="cluster-panel")
            ]),

                dbc.Col(md=9, children=[
                #html.Div(id="cluster-title"),
                dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="buttom-plot-kgs"), label="Wassla l3dm / Total kgs"),
                dbc.Tab(dcc.Graph(id="buttom-plot"), label="Wassla l3dm / Total shipment"),
                dbc.Tab(dcc.Graph(id="buttom-plot-price"), label="Wassla l3dm / Total price"),
                dbc.Tab(dcc.Graph(id="buttom-plot-volume"), label="Wassla l3dm / Total volume"),
                dbc.Tab(dcc.Graph(id=".."), label="....")
                
            ])
                        ])
            ]
        ),
        dbc.Row([
        ### input + panel
        dbc.Col(md=3, children=[
           customer_input
        ]),
        ### plots
        ### plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("ML Analysis"), width={"size":6,"offset":3})
            # dbc.Tabs(className="nav nav-pills", children=[
            #     dbc.Tab(dcc.Graph(id="k-means"), label="K-means Clustering"),
            #     dbc.Tab(dcc.Graph(id="plot-active"), label="Hierarchical Clustering")
                
            # ])
        ])
        
                
    ])

])




#Python function to plot panel 
@app.callback(output=Output("cluster-insight","children"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_title(cluster_panel,dataframe):
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    info = data.get_info(d)
    panel = html.Div([
        html.H4('Characteristics of Cluster {}'.format(cluster_panel)),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            
            html.H6("mean || Total Price:", style={"color":"white"}),
            html.H3("{:,.0f}".format(info[1]), style={"color":"white"}),
            
            html.H6("mean || Total Shipments:", className="text-danger"),
            html.H3("{:,.0f}".format(info[0]), className="text-danger"),
            
            # html.H6("Best Customer:", style={"color":"white"}),
            # html.H3("{:,.0f}".format(active_cases_today), style={"color":"white"}),
            
            # html.H6("Worst Customer:", className="text-danger"),
            # html.H3("{:,.0f}".format(active_cases_in_30days), className="text-danger"),
            
            # html.H6("Peak day:", style={"color":peak_color}),
            # html.H3(peak_day.strftime("%Y-%m-%d"), style={"color":peak_color}),
            # html.H6("with {:,.0f} cases".format(num_max), style={"color":peak_color})
        
        ])
    ])
    return panel


# Python function to plot Histogram
# @app.callback(output=Output("plot-total","figure"), inputs=[Input("feature","value")]) 
# def plot_total_cases(feature):
#     d=data.df
#     chart = Chart()
#     return chart.plot_hist(d,feature)

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


#Top plot 
@app.callback(output=Output("top-plot","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_bsh(cluster_panel,dataframe):
    #print(dataframe)    
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_top_shps(d)  
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,True)

@app.callback(output=Output("top-plot-kgs","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_tkg(cluster_panel,dataframe):
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_top_kgs(d)
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,True)

@app.callback(output=Output("top-plot-volume","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_tvolume(cluster_panel,dataframe):
    #print(dataframe)    
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_top_volume(d)  
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,True)

@app.callback(output=Output("top-plot-price","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_tprice(cluster_panel,dataframe):
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_top_price(d)
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,True)

#bottom plot 
@app.callback(output=Output("buttom-plot","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_bsh(cluster_panel,dataframe):
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_buttom_shps(d)
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,False)

@app.callback(output=Output("buttom-plot-kgs","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_bkg(cluster_panel,dataframe):
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_buttom_kgs(d)
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,False)

@app.callback(output=Output("buttom-plot-volume","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_tvolume(cluster_panel,dataframe):
    #print(dataframe)    
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_buttom_volume(d)  
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,False)

@app.callback(output=Output("buttom-plot-price","figure"), inputs=[Input("cluster-panel","value"),Input("dataframe","value")])
def render_cluster_plot_tprice(cluster_panel,dataframe):
    # print(cluster_panel," ",type(cluster_panel))
    d= data.get_shp_cluster_name(cluster_panel,dataframe)
    details = data.get_buttom_price(d)
    # clu_int = int(cluster_panel)
    chart = Chart()
    return chart.plot_h_top(details,False)

# Plot scatter
@app.callback(output=Output("k-means","figure"), inputs=[Input("dataframe","value")]) 
def plot_k_means(dataframe):
    #print(type(dataframe))
    pca_df = data.get_pca(dataframe)   
    chart = Chart()
    return chart.plot_scatter(pca_df)


# Plot cluster's general insights 
@app.callback(output=Output("horizontal-bar","figure"), inputs=[Input("dataframe","value")]) 
def plot_h_cluster(dataframe):
    #print(type(dataframe))
    pca_df = data.get_pca(dataframe)
    chart = Chart()
    return chart.plot_h_bar(pca_df)

#dropdown cluster 
@app.callback(output=Output("cluster-panel","children"), inputs=[Input("dataframe","value")])
def render_output_panel(dataframe):
    x_df = data.get_pca(dataframe)
    clusters = x_df.cluster.unique().tolist()
    panel = html.Div([
    dbc.FormGroup([
    html.H4("Select Cluster"),
    dcc.Dropdown(id="cluster-panel", options=[{"label":x,"value":x} for x in clusters], value="0")
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