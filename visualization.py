from plotly import graph_objects as go
import plotly.express as px
import numpy as np



def plotBar(x, y, title="default title", xlabel="", ylabel=""):
    # Use the hovertext kw argument for hover text
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    # Customize aspect
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text=title)

    return fig
