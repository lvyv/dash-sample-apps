from dash import dcc
from dash import html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_current_prices = pd.read_csv(DATA_PATH.joinpath("df_current_prices.csv"))
df_hist_prices = pd.read_csv(DATA_PATH.joinpath("df_hist_prices.csv"))
df_avg_returns = pd.read_csv(DATA_PATH.joinpath("df_avg_returns.csv"))
df_after_tax = pd.read_csv(DATA_PATH.joinpath("df_after_tax.csv"))
df_recent_returns = pd.read_csv(DATA_PATH.joinpath("df_recent_returns.csv"))
df_graph = pd.read_csv(DATA_PATH.joinpath("df_graph2.csv"))
df_graph['Date'] = pd.to_datetime(df_graph['Date'])


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                    # Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["屏蔽泵主要参数"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(df_current_prices)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["泵特征曲线"],
                                        className="subtitle padded",
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("pump-fig1.png"),
                                        className="risk-reward",
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("长期性能曲线趋势图", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-4",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_graph["Date"],
                                                    y=df_graph["Calibre Index Fund"],
                                                    line={"color": "#2879ff"},
                                                    mode="lines",
                                                    name="实测曲线",
                                                ),
                                                go.Scatter(
                                                    x=df_graph["Date"],
                                                    y=df_graph[
                                                        "MSCI EAFE Index Fund (ETF)"
                                                    ],
                                                    line={"color": "#a6d854"},
                                                    mode="lines",
                                                    name="理论曲线",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=700,
                                                height=200,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                showlegend=True,
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                xaxis={
                                                    "autorange": True,
                                                    "nticks": 10,
                                                    "range": [
                                                        "2007-12-31",
                                                        "2018-03-06",
                                                    ],
                                                    "rangeselector": {
                                                        "buttons": [
                                                            {
                                                                "count": 1,
                                                                "label": "1个月",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 3,
                                                                "label": "3个月",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 5,
                                                                "label": "5个月",
                                                                "step": "month",
                                                            },
                                                            {
                                                                "count": 10,
                                                                "label": "10个月",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "label": "全部",
                                                                "step": "all",
                                                            },
                                                        ]
                                                    },
                                                    "showline": True,
                                                    "type": "date",
                                                    "zeroline": False,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        18.6880162434,
                                                        278.431996757,
                                                    ],
                                                    "showline": True,
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={
                                            "displayModeBar": False,
                                            "locale": "de-CH"
                                        },
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        [
                                            "装备关键统计量分析"
                                        ],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(df_avg_returns),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["压力-流量特征曲线"],
                                        className="subtitle padded",
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("pump-fig2.png"),
                                        className="risk-reward",
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # # Row 4
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.H6(
                    #                     [
                    #                         "数据处理前预分析--本分析每季度更新一次，时间：12/31/2017"
                    #                     ],
                    #                     className="subtitle padded",
                    #                 ),
                    #                 html.Div(
                    #                     [
                    #                         html.Table(
                    #                             make_dash_table(df_after_tax),
                    #                             className="tiny-header",
                    #                         )
                    #                     ],
                    #                     style={"overflow-x": "auto"},
                    #                 ),
                    #             ],
                    #             className=" twelve columns",
                    #         )
                    #     ],
                    #     className="row ",
                    # ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["最近一次统计量"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table(df_recent_returns),
                                        className="tiny-header",
                                    ),
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
