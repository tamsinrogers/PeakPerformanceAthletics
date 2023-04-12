import json
import plotly
import plotly.express as px


def pie_chart(data: list, title: str, labels: list[str]):
    '''Create plotly pie chart and return as JSON'''

    fig = px.pie(values=data,
                 labels=labels,
                 hole=.5,
                 title=title)

    colors = ['black', 'darkblue', 'white']

    fig.update_traces(marker=dict(colors=colors,
                                  line=dict(color='#000000', width=2)))

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })

    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30),
                      showlegend=False,
                      width=300,
                      height=300,
                      font_color="white")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def line_chart(x: list, y: list, title: str):

    fig = px.scatter(x=x, y=y, title=title)

    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })

    fig.update_layout(margin=dict(l=30, r=30, t=100, b=30),
                      showlegend=False,
                      width=1000,
                      height=300,
                      font_color="white")

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
