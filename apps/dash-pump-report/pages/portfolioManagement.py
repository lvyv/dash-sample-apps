from dash import dcc
from dash import html
import plotly.graph_objs as go

from utils import Header, make_dash_table
import pandas as pd
import pathlib

# pump
# https://www.csidesigns.com/blog/articles/how-to-read-a-pump-curve


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_equity_char = pd.read_csv(DATA_PATH.joinpath("df_equity_char.csv"))
df_equity_diver = pd.read_csv(DATA_PATH.joinpath("df_equity_diver.csv"))


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 3
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [html.H6(["额定功率测试"], className="subtitle padded")],
                                className="twelve columns",
                            )
                        ],
                        className="rows",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(["试验方法"], style={"color": "#7a7a7a"}),
                                    dcc.Graph(
                                        id="graph-5",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=["1"],
                                                    y=["1"],
                                                    hoverinfo="none",
                                                    marker={"opacity": 0},
                                                    mode="markers",
                                                    name="B",
                                                )
                                            ],
                                            "layout": go.Layout(
                                                title="",
                                                annotations=[
                                                    {
                                                        "x": 0.990130093458,
                                                        "y": 1.00181709504,
                                                        "align": "left",
                                                        "font": {
                                                            "family": "Raleway, sans-serif",
                                                            "size": 7,
                                                            "color": "#7a7a7a",
                                                        },
                                                        "showarrow": False,
                                                        "text": "<b>Market<br>Cap</b>",
                                                        "xref": "x",
                                                        "yref": "y",
                                                    },
                                                    {
                                                        "x": 1.00001816013,
                                                        "y": 1.35907755794e-16,
                                                        "font": {
                                                            "family": "Raleway, sans-serif",
                                                            "size": 7,
                                                            "color": "#7a7a7a",
                                                        },
                                                        "showarrow": False,
                                                        "text": "<b>Style</b>",
                                                        "xref": "x",
                                                        "yanchor": "top",
                                                        "yref": "y",
                                                    },
                                                ],
                                                autosize=False,
                                                width=200,
                                                height=150,
                                                hovermode="closest",
                                                margin={
                                                    "r": 30,
                                                    "t": 20,
                                                    "b": 20,
                                                    "l": 30,
                                                },
                                                shapes=[
                                                    {
                                                        "fillcolor": "#f9f9f9",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0,
                                                        "x1": 0.33,
                                                        "xref": "paper",
                                                        "y0": 0,
                                                        "y1": 0.33,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f2f2f2",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "dash": "solid",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0.33,
                                                        "x1": 0.66,
                                                        "xref": "paper",
                                                        "y0": 0,
                                                        "y1": 0.33,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f9f9f9",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0.66,
                                                        "x1": 0.99,
                                                        "xref": "paper",
                                                        "y0": 0,
                                                        "y1": 0.33,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f2f2f2",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0,
                                                        "x1": 0.33,
                                                        "xref": "paper",
                                                        "y0": 0.33,
                                                        "y1": 0.66,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f9f9f9",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0.33,
                                                        "x1": 0.66,
                                                        "xref": "paper",
                                                        "y0": 0.33,
                                                        "y1": 0.66,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f2f2f2",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0.66,
                                                        "x1": 0.99,
                                                        "xref": "paper",
                                                        "y0": 0.33,
                                                        "y1": 0.66,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f9f9f9",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0,
                                                        "x1": 0.33,
                                                        "xref": "paper",
                                                        "y0": 0.66,
                                                        "y1": 0.99,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": " #97151c",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0.33,
                                                        "x1": 0.66,
                                                        "xref": "paper",
                                                        "y0": 0.66,
                                                        "y1": 0.99,
                                                        "yref": "paper",
                                                    },
                                                    {
                                                        "fillcolor": "#f9f9f9",
                                                        "line": {
                                                            "color": "#ffffff",
                                                            "width": 0,
                                                        },
                                                        "type": "rect",
                                                        "x0": 0.66,
                                                        "x1": 0.99,
                                                        "xref": "paper",
                                                        "y0": 0.66,
                                                        "y1": 0.99,
                                                        "yref": "paper",
                                                    },
                                                ],
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        0.989694747864,
                                                        1.00064057995,
                                                    ],
                                                    "showgrid": False,
                                                    "showline": False,
                                                    "showticklabels": False,
                                                    "title": "<br>",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        -0.0358637178721,
                                                        1.06395696354,
                                                    ],
                                                    "showgrid": False,
                                                    "showline": False,
                                                    "showticklabels": False,
                                                    "title": "<br>",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="four columns",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "电机输出功率额定，屏蔽泵设置按照标准工况要求设置，调校系统达到最佳工作状态进行试验。"
                                    ),
                                    html.P(
                                        "试验进行多次，试验每次持续20分钟，并利用物联网系统详细采集组态系统参数和值，采集振动数据。"
                                    ),
                                ],
                                className="eight columns middle-aligned",
                                style={"color": "#696969"},
                            ),
                        ],
                        className="row ",
                    ),
                    # Row 3
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["试验过程事件"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table(df_equity_char),
                                        className="tiny-header",
                                    ),
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["观察指标记录"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table(df_equity_diver),
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
