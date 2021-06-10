from re import template
from plotly import graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib as plt


def plotBar(x, y, title="Bar Chart showing the count of tweets ", xlabel="", ylabel=""):
    # Use the hovertext kw argument for hover text
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    # Customize aspect
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text=title)

    return fig


def plotHistogram(dataframe, x, title="A Histogram determining the subjectivity of the tweets"):
    # Use the hovertext kw argument for hover text
    fig = px.histogram(dataframe, x=x, nbins=10,
                       title=title,
                       labels={x: x},  # can specify one label per df column
                       opacity=0.8,
                       log_y=True,  # represent bars with log scale
                       # color of histogram bars
                       color_discrete_sequence=['indianred']
                       )

    return fig

def plotpie(labels, values, title):
    layout = go.Layout(title=title, template="plotly_dark")
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Pie(labels=labels, values=values, textinfo='label+percent', hole=0.2,
                         marker=dict(colors=['#f7d468', '#74cb35'],
                                     line_color='Gray',
                                     line_width=1),
                         textfont={'color': '#000', 'size': 12},
                         textfont_size=12))
    return fig