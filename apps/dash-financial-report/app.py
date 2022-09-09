# -*- coding: utf-8 -*-
import dash
import glob
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
)
app.title = "复盘与评估"
server = app.server


event_file_list = glob.glob("data/*.csv")
event_files = [w.replace("data\\", "") for w in event_file_list]
event_files = [s for s in event_files if "统计" in s]

# Create list of tracking json files available to select from via a pulldown menu
tracking_file_list = glob.glob("data/*.json")
tracking_files = [w.replace("data\\", "") for w in tracking_file_list]
tracking_files = [s for s in tracking_files if "json" in s]
# Cost Metric
play_team = [
    "红方",
    "蓝方"
]
# Describe the layout/ UI of the app
app.layout = html.Div(
    [
        html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                id="events",
                                className="select-outer",
                                children=[
                                    html.Label("演训事件文件："),
                                    dcc.Dropdown(
                                        id="event-file",
                                        options=[{"label": i, "value": i} for i in event_files],
                                        value=None,
                                        placeholder="选择演训事件文件",
                                    ),
                                ],
                            ),
                            html.Div(
                                id="teams",
                                className="select-outer",
                                children=[
                                    html.Label("演训队伍:"),
                                    dcc.Dropdown(
                                        id="team-dropdown",
                                        options=[{"label": i, "value": i} for i in play_team],
                                        value=None,
                                        placeholder="选择演训队伍",
                                    ),
                                ],
                            ),
                            html.Div(
                                id="traces",
                                className="select-outer",
                                children=[
                                    html.Label("演训日志数据:"),
                                    dcc.Dropdown(
                                        id="tracking-file",
                                        options=[{"label": i, "value": i} for i in tracking_files],
                                        value=None,
                                        placeholder="选择复盘演训数据文件",
                                        # className="four columns"
                                    ),
                                    daq.Knob(  # noqa
                                        id="speed-knob",
                                        label="复盘速度",
                                        value=2.5,
                                        max=5,
                                        color={"default": "#3598DC"},
                                        size=50,
                                    ),
                                    html.Button("提交", id="submit-button", className='btn-ele'),
                                ],
                            ),
                        ],
                        className="three columns",
                    ),
                    dcc.Loading(
                        id="loading-icon7",
                        # className="nine columns",
                        children=[
                            dcc.Graph(
                                id="game-simulation",
                                animate=True,
                                figure=initial_figure_simulator(),
                                className="simulation-graph",
                                config={
                                    "modeBarButtonsToAdd": [
                                        "drawline",
                                        "drawopenpath",
                                        "drawcircle",
                                        "drawrect",
                                        "eraseshape",
                                    ],
                                    "modeBarButtonsToRemove": [
                                        "toggleSpikelines",
                                        "pan2d",
                                        "autoScale2d",
                                        "resetScale2d",
                                    ],
                                    "displaylogo": False,
                                },
                            )
                        ],
                        type="default",
                    )
                ],
                className="control-row-1 control-panel",
        ),
        html.Div(
            className="control-row-2",
            children=[
                dcc.Location(id="url", refresh=False),
                html.Div(id="page-content")
            ],
        ),
    ]
)


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/price-performance":
        return pricePerformance.create_layout(app)
    elif pathname == "/dash-financial-report/portfolio-management":
        return portfolioManagement.create_layout(app)
    elif pathname == "/dash-financial-report/fees":
        return feesMins.create_layout(app)
    elif pathname == "/dash-financial-report/distributions":
        return distributions.create_layout(app)
    elif pathname == "/dash-financial-report/news-and-reviews":
        return newsReviews.create_layout(app)
    elif pathname == "/dash-financial-report/full-view":
        return (
            overview.create_layout(app),
            pricePerformance.create_layout(app),
            portfolioManagement.create_layout(app),
            feesMins.create_layout(app),
            distributions.create_layout(app),
            newsReviews.create_layout(app),
        )
    else:
        return overview.create_layout(app)


# Callback for KPI Radar
@app.callback(
    Output("radar-graph", "figure"),
    [Input("event-file", "value"), Input("team-dropdown", "value")],
    prevent_initial_call=True,
)
def radar_graph(radar_file, team):
    if team is not None:
        fig = team_radar_builder(radar_file, team)
        return fig
    else:
        fig = initial_figure_radar()
        fig.update_layout(margin=dict(l=80, r=80, b=30, t=55))
        # Disable zoom. It just distorts and is not fine-tunable
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        return fig


# Callback for animated game simulation graph
@app.callback(
    Output("game-simulation", "figure"),
    Input("submit-button", "n_clicks"),
    State("speed-knob", "value"),
    State("tracking-file", "value"),
    prevent_initial_call=True,
)
def game_simulation(n_clicks, speed, filename):
    print(n_clicks)
    speed_adjusted = speed * 100
    game_speed = 600 - speed_adjusted
    fig = fig_from_json("data/" + filename)  # noqa
    fig.update_layout(margin=dict(l=0, r=20, b=0, t=0))
    fig.update_layout(newshape=dict(line_color="#009BFF"))
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = game_speed
    fig.update_yaxes(scaleanchor="x", scaleratio=0.70)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=-0.10,
                x=-0.08,
                xanchor="left",
                yanchor="bottom",
            )
        ]
    )
    fig.update_layout(autosize=True)
    fig.update_layout(modebar=dict(bgcolor="rgba(0, 0, 0, 0)", orientation="v"))
    # Disable zoom. It just distorts and is not fine-tunable
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout(legend=dict(font=dict(family="Arial", size=10, color="grey")))
    # Sets background to be transparent
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(showgrid=False, showticklabels=False),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )
    fig["layout"]["template"]["data"]["scatter"][0]["marker"]["line"]["color"] = "white"
    fig["layout"]["template"]["data"]["scatter"][0]["marker"]["opacity"] = 0.9
    return fig


if __name__ == "__main__":
    app.run_server()
