from dash import html
from utils import Header, make_dash_table
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_dividend = pd.read_csv(DATA_PATH.joinpath("df_dividend.csv"))
df_realized = pd.read_csv(DATA_PATH.joinpath("df_realized.csv"))
df_unrealized = pd.read_csv(DATA_PATH.joinpath("df_unrealized.csv"))


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["综合通信结论"], className="subtitle padded"
                                    ),
                                    html.P(
                                        [
                                            "Distributions for this fund are scheduled quaterly"
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["试验目标事件"],
                                        className="subtitle tiny-header padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(df_dividend),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
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
                                        ["试验过程事件"],
                                        className="subtitle tiny-header padded",
                                    )
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
                                [html.Table(make_dash_table(df_realized))],
                                className="six columns",
                            ),
                            html.Div(
                                [html.Table(make_dash_table(df_unrealized))],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
