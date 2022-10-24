from dash import dcc
from dash import html
from utils import initial_figure_radar
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("XC-JZ-L701泵健康评估报告"),
                                    html.Br([]),
                                    html.Div([
                                        html.Div([
                                            html.P('【报告结论】：'),
                                        ], className='two columns'),
                                        html.Div([
                                            html.P('健康', style={
                                                'textAlign': 'left',
                                                'font-size': 'large',
                                                'font-weight': 'bold',
                                                'color': '#a6d854'}),
                                        ], className='six columns'),
                                        html.Div([
                                            html.P('【报告时间】：2022.09.10'),
                                        ], className='four columns'),
                                    ], className="row"),
                                    html.P(
                                        "\
                                    对XC-JZ-L701泵进行综合健康评估，健康评估指标包含7项，数据来自3次试验测试值经健康评估模型\
                                    计算得出的试验测试指标数据和日常运维数据经健康评估模型综合分析得出的历史评估指标。\
                                    试验评估指标包含：扬程、流量、输入功率、转速共四项，均为模拟标准工况下的实际测量值数据。\
                                    历史评估指标包含：振动综合指标、BEP变化率、服役期间保养共三项，均为历史数据分析计算得出。\
                                    健康评估指标最终按专家赋予权值综合为健康状态值，可分类为1~5个级别，对应不同的运行风险。\
                                    其分别对应报告结论的：第1级——健康，第2级——亚健康，第3级——关注，第4级——告警，第5级——高风险。\
                                    不同时间计算的健康状态值被系统持续跟踪，并据此支持用户从长期视角看到装备健康状态的变化情况。",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["评估指标"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(df_fund_facts)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "评估指标雷达图",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="radar-graph",
                                        figure=initial_figure_radar(),

                                        config={
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ],
                                            "displaylogo": False
                                        },
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "装备健康状态演变趋势图",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="health_trends_graph",
                                        style={"height": "500px"}
                                        # figure=linechart_builder(XX, YY, YY_upper, YY_lower),
                                        # config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "本次试验统计量 ",
                                                className="subtitle padded",
                                            ),
                                            html.Table(make_dash_table(df_price_perf)),
                                        ],
                                        className="twelve columns",
                                    ),
                                    html.Div(
                                        [
                                            html.H6(
                                                "潜在风险", className="subtitle padded"
                                            ),
                                            html.Img(
                                                src=app.get_asset_url("risk_reward.png"),
                                                className="risk-reward",
                                            ),
                                        ],
                                        className="twelve columns",
                                    )],
                                className="six columns"),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
