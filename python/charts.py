import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np 

class Chart():
    
    @staticmethod
    def plot_hist(df,feature):

        fig = go.Figure()
        column = df[[feature]].squeeze('columns')

        fig.add_trace(go.Histogram(x=column,marker_color='#330C73'))
        
        
        ## add slider
        fig.update_xaxes(rangeslider_visible=True)    
        ## set background color
        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=550)        
         
        return fig 

    @staticmethod
    def plot_scatter(df) : 
        
        fig = px.scatter(df, x="pca1", y="pca2", color="cluster")
        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=400) 
        return fig 

    @staticmethod
    def plot_pie(df) : 
        
        colors = ['#1b078d','#7d07a6','#cb4779','#f89640','#f0f921']
        fig = px.pie(df, values='cluster', names='cluster', color="cluster",
             color_discrete_map={'0':'#1b078d',
                                 '1':'#7d07a6',
                                 '2':'#cb4779',
                                 '3':'#f89640',
                                 '4' :'#f0f921'   }
            )
        #fig.update_traces(marker=dict(colors=colors))
        fig.update_layout(plot_bgcolor='white', autosize=False, width=500, height=500) 
        return fig 

    @staticmethod
    def plot_h_bar(df) : 
        
        count_cluster = df['cluster'].value_counts().tolist()
        y_clusters = ['cluster1','cluster0','cluster4','cluster3','cluster2']

        fig = go.Figure(go.Bar(
         x=count_cluster,
         y=y_clusters,
            marker=dict(
                color='#9CC0E7',
                line=dict(
                    color='#FFFFFF',
                    width=1)
            ),
            orientation='h',
        ))

        #fig.update_traces(marker=dict(colors=colors))
        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=400) 
        return fig

    # @staticmethod
    # def plot_2h_bar(df) :
        
    #     fig2 = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
    #                 shared_yaxes=False, vertical_spacing=0.001)

    #     fig2.append_trace(go.Bar(
    #         x=top_cust_shp,
    #         y=top_cust_name,
    #         marker=dict(
    #             color='rgba(50, 171, 96, 0.6)',
    #             line=dict(
    #                 color='rgba(50, 171, 96, 1.0)',
    #                 width=1),
    #         ),
    #         orientation='h',
    #     ), 1, 1)

    #     fig2.append_trace(go.Bar(
    #         x=top_cust_kg,
    #         y=top_cust_kg_name,
    #         marker=dict(
    #             color='rgba(50, 171, 96, 0.6)',
    #             line=dict(
    #                 color='rgba(50, 171, 96, 1.0)',
    #                 width=1),
    #         ),
    #         orientation='h',
    #     ), 1, 2)

    #     #fig.update_traces(marker=dict(colors=colors))
    #     fig2.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=400) 
    #     return fig2
    
    @staticmethod
    def plot_h_top(details,info) : 

        if info : 
            color = '#22bb33'
        else : 
            color = '#bb2124'
        fig = go.Figure(go.Bar(
         x=details[0],
         y=details[1],
            marker=dict(
                color=color,
                line=dict(
                    color='#FFFFFF',
                    width=1)
            ),
            orientation='h',
        ))

        #fig.update_traces(marker=dict(colors=colors))
        fig.update_layout(plot_bgcolor='white', autosize=False, width=1000, height=400) 
        return fig
