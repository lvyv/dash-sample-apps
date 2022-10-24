# -*- coding: utf-8 -*-
import locale
from datetime import datetime
import dash
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from pages import (
    overview,
    pricePerformance,
    portfolioManagement,
    feesMins,
    distributions,
    newsReviews,
)
from utils import initial_figure_radar, team_radar_builder, initial_figure_simulator, fig_from_json
import dash_daq as daq

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True
)
app.title = "健康评估报告应用"
server = app.server

XX = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

YY_upper = [100, 100, 98, 97.5, 96.5, 97, 96, 99, 96, 95, 99]
YY = [98.5, 99.5, 95, 89.5, 92, 96, 95.5, 98, 93, 94.5, 95.5]
YY_lower = [89.5, 90, 88, 88.5, 90.5, 93, 93, 92, 90, 92, 94]
YY_lower = YY_lower[::-1]
# event_file_list = glob.glob("data/*.csv")
# event_files = [w.replace("data\\", "") for w in event_file_list]
# event_files = [s for s in event_files if "统计" in s]

# Create list of tracking json files available to select from via a pulldown menu
# tracking_file_list = glob.glob("data/*.json")
# tracking_files = [w.replace("data\\", "") for w in tracking_file_list]
# tracking_files = [s for s in tracking_files if "json" in s]
# # Cost Metric
# play_team = [
#     "红方",
#     "蓝方"
# ]
# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-pump-report/price-performance":
        return pricePerformance.create_layout(app)
    elif pathname == "/dash-pump-report/portfolio-management":
        return portfolioManagement.create_layout(app)
    elif pathname == "/dash-pump-report/fees":
        return feesMins.create_layout(app)
    elif pathname == "/dash-pump-report/distributions":
        return distributions.create_layout(app)
    elif pathname == "/dash-pump-report/news-and-reviews":
        return newsReviews.create_layout(app)
    elif pathname == "/dash-pump-report/full-view":
        return (
            overview.create_layout(app),
            pricePerformance.create_layout(app),
            # portfolioManagement.create_layout(app),
            # feesMins.create_layout(app),
            # distributions.create_layout(app),
            # newsReviews.create_layout(app),
        )
    else:
        return overview.create_layout(app)


@app.callback(Output("health_trends_graph", "figure"), [Input("url", "pathname")])
def linechart_builder(abc):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=XX+XX[::-1],
        y=YY_upper+YY_lower,
        fill='toself',
        fillcolor='rgba(0,176,246, 0.2)',
        line_color='rgba(255,255,255,0)',
        name='同类型',
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=XX, y=YY,
        line_color='#2879ff',
        name='XC-JZ-L701健康状态值'
    ))
    fig.update_traces(mode='lines')
    fig.update_layout(
        autosize=True,

        title="",
        font={"family": "Raleway", "size": 10},
        height=300,
        width=340,
        hovermode="closest",
        legend={
            "x": -0.0277108433735,
            "y": -0.142606516291,
            "orientation": "h",
        },
        margin={
            "r": 20,
            "t": 20,
            "b": 20,
            "l": 50,
        },
        showlegend=True,
        xaxis={
            "autorange": True,
            "linecolor": "rgb(0, 0, 0)",
            "linewidth": 1,
            "nticks": 12,
            "range": [0, 12],
            "showgrid": False,
            "showline": True,
            "title": "月",
            "type": "linear",
        },
        yaxis={
            "autorange": False,
            "gridcolor": "rgba(127, 127, 127, 0.2)",
            "mirror": False,
            "nticks": 8,
            "range": [85, 100],
            "showgrid": True,
            "showline": True,
            "ticklen": 10,
            "ticks": "outside",
            "title": "健康状态值",
            "type": "linear",
            "zeroline": False,
            "zerolinewidth": 4,
        },
    )
    return fig
# Callback for KPI Radar
# @app.callback(
#     Output("radar-graph", "figure"),
#     [Input("event-file", "value"), Input("team-dropdown", "value")],
#     prevent_initial_call=False,
# )
# def radar_graph(radar_file, team):
#     if team is not None:
#         fig = team_radar_builder(radar_file, team)
#         return fig
#     else:
#         fig = initial_figure_radar()
#         fig.update_layout(margin=dict(l=80, r=80, b=30, t=55))
#         # Disable zoom. It just distorts and is not fine-tunable
#         fig.layout.xaxis.fixedrange = True
#         fig.layout.yaxis.fixedrange = True
#         return fig


# Callback for animated game simulation graph
# @app.callback(
#     Output("game-simulation", "figure"),
#     Input("submit-button", "n_clicks"),
#     State("speed-knob", "value"),
#     State("tracking-file", "value"),
#     prevent_initial_call=True,
# )
# def game_simulation(n_clicks, speed, filename):
#     print(n_clicks)
#     speed_adjusted = speed * 100
#     game_speed = 600 - speed_adjusted
#     fig = fig_from_json("data/" + filename)  # noqa
#     fig.update_layout(margin=dict(l=0, r=20, b=0, t=0))
#     fig.update_layout(newshape=dict(line_color="#009BFF"))
#     fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = game_speed
#     fig.update_yaxes(scaleanchor="x", scaleratio=0.70)
#     fig.update_layout(
#         updatemenus=[
#             dict(
#                 type="buttons",
#                 showactive=False,
#                 y=-0.10,
#                 x=-0.08,
#                 xanchor="left",
#                 yanchor="bottom",
#             )
#         ]
#     )
#     fig.update_layout(autosize=True)
#     fig.update_layout(modebar=dict(bgcolor="rgba(0, 0, 0, 0)", orientation="v"))
#     # Disable zoom. It just distorts and is not fine-tunable
#     fig.layout.xaxis.fixedrange = True
#     fig.layout.yaxis.fixedrange = True
#     fig.update_layout(legend=dict(font=dict(family="Arial", size=10, color="grey")))
#     # Sets background to be transparent
#     fig.update_layout(
#         template="plotly_dark",
#         xaxis=dict(showgrid=False, showticklabels=False),
#         plot_bgcolor="rgba(0, 0, 0, 0)",
#         paper_bgcolor="rgba(0, 0, 0, 0)",
#     )
#     fig["layout"]["template"]["data"]["scatter"][0]["marker"]["line"]["color"] = "white"
#     fig["layout"]["template"]["data"]["scatter"][0]["marker"]["opacity"] = 0.9
#     return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
