from dash import html
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
import pathlib

REDTROOP = '红方'
BLUETROOP = '蓝方'
RADAR_HEADERS = [
    "流量（工况）",
    "输入功率（工况）",
    "转速（工况）",
    "振动综合指标",
    "BEP变化率",
    "服役期间保养",
    "指标B",
    "指标C",
    "指标D",
    "扬程（工况）",
]


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [

            html.Div(
                [
                    html.Div(
                        [html.H5("XC旋转机械类健康评估报告")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "全文视图",
                                href="/dash-pump-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "总结",
                href="/dash-pump-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "综合分析",
                href="/dash-pump-report/price-performance",
                className="tab",
            ),
            # dcc.Link(
            #     "附件1",
            #     href="/dash-pump-report/portfolio-management",
            #     className="tab",
            # ),
            # dcc.Link(
            #     "附件2", href="/dash-pump-report/fees", className="tab"
            # ),
            # dcc.Link(
            #     "附件3",
            #     href="/dash-pump-report/distributions",
            #     className="tab",
            # ),
            # dcc.Link(
            #     "附件4",
            #     href="/dash-pump-report/news-and-reviews",
            #     className="tab",
            # ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


# Create initial placeholder figure for radar plot
def initial_figure_radar():
    fig = go.Figure()
    r_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    fig.add_trace(
        go.Scatterpolar(
            r=r_values,
            theta=RADAR_HEADERS,
            fill="toself",
            opacity=0.50,
        )
    )
    fig = team_radar_builder('红箭22军演统计.csv', '蓝方')
    fig.update_layout(
        # template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )

    fig.update_layout(modebar=dict(bgcolor="rgba(0, 0, 0, 0)"))

    fig.update_layout(
        polar=dict(
            bgcolor="#282828",
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, ),
        ),
        showlegend=False,
    )

    fig.update_layout(margin=dict(l=60, r=60, b=30, t=45))
    fig.update_layout(height=240)
    return fig


# 'Normalize' values (not in a traditional sense, but in terms of percentages during the match)
def normalize_events(df):
    # Rename and trim down the df to columns we want
    df = df.set_index("Team")
    df = df[
        [
            "SET PIECE",
            "PASS",
            "BALL LOST",
            "RECOVERY",
            "CHALLENGE",
            "SHOT",
            "INTERCEPTION",
            "CROSS",
            "DEEP BALL",
            "FREE KICK",
        ]
    ]
    df.columns = RADAR_HEADERS

    # 'Normalize' values from different scales by scaling them as a percentage of max. Use try/except to
    # avoid division by zero
    try:
        df_normalized = df / (df.max() + df.min())
    except:
        df_normalized = (df + 0.1) / (df.max() + df.min())

    # Replace nan's with zeros
    standard_df_normalized = df_normalized.fillna(0)
    return df_normalized


# Main function
def team_radar_builder(filename, team_id):
    # Read in the events data file
    data_file = pathlib.Path(__name__).parent.joinpath("data").joinpath(filename).resolve()
    events_df = pd.read_csv(data_file, encoding='utf8', engine="python")
    events_df = events_df[["Team", "Type", "Subtype"]]

    # Count up the events for each team and create a new pivoted dataframe to hold the results
    type_counted_df = (
        events_df.groupby(["Team", "Type"]).size().to_frame("count").reset_index()
    )
    subtype_counted_df = (
        events_df.groupby(["Team", "Subtype"]).size().to_frame("count").reset_index()
    )
    df1_pivoted = pd.pivot_table(
        type_counted_df, values="count", index="Team", columns=["Type"], aggfunc=sum
    ).reset_index()
    df2_pivoted = pd.pivot_table(
        subtype_counted_df,
        values="count",
        index="Team",
        columns=["Subtype"],
        aggfunc=sum,
    ).reset_index()
    df_pivoted = pd.merge(df1_pivoted, df2_pivoted, on="Team")
    df_pivoted = df_pivoted.fillna(0)
    normalized_df = normalize_events(df_pivoted)

    theta_values = list(normalized_df.columns)

    # Create initial figure
    fig = go.Figure()
    colormap = {REDTROOP: "red", BLUETROOP: "blue"}
    normalized_df["Team"] = normalized_df.index
    team_row_normalized = normalized_df.loc[normalized_df["Team"] == team_id]
    team_row_normalized.drop("Team", axis=1, inplace=True)
    team_row = team_row_normalized.reset_index(drop=True)
    r_values = team_row.iloc[0].values.flatten().tolist()

    # Providing a way to use normalized values for the graph but actual values for hover
    team_row_value = df_pivoted.loc[df_pivoted["Team"] == team_id]
    team_row_value.drop("Team", axis=1, inplace=True)
    team_row_value = team_row_value[
        [
            "SET PIECE",
            "PASS",
            "BALL LOST",
            "RECOVERY",
            "CHALLENGE",
            "SHOT",
            "INTERCEPTION",
            "CROSS",
            "DEEP BALL",
            "FREE KICK",
        ]
    ]
    team_row_value = team_row_value.reset_index(drop=True)
    pki_values = team_row_value.iloc[0].values.flatten().tolist()

    fig.add_trace(
        go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            fill="toself",
            name=team_id,
            opacity=0.5,
            fillcolor='#2879ff',
            hovertext=pki_values,
            hovertemplate="%{theta}:" + " %{hovertext}<br>",
        )
    )

    # Making some small markers that users can hover over to get more info (else they might not know where to hover)
    fig.update_traces(
        mode="lines+markers",
        line_color=colormap[team_id],
        marker=dict(color="white", symbol="circle", size=4),
    )

    # fig.update_layout(
    #     # title="演训KPI指标",
    #     polar=dict(
    #         bgcolor="#2A2A2A",
    #         radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, ),
    #     ),
    #     showlegend=False,
    #     autosize=False,
    # )
    #
    # fig.update_layout(
    #     # template="plotly_dark",
    #     plot_bgcolor="rgba(0, 0, 0, 0)",
    #     paper_bgcolor="rgba(0, 0, 0, 0)",
    # )
    #
    # fig.update_layout(modebar=dict(bgcolor="rgba(0, 0, 0, 0)"))
    # fig.update_layout(margin=dict(l=55, r=55, b=30, t=45))

    return fig


# Create initial placeholder figure for game simulator
def initial_figure_simulator():
    # fig = px.scatter(x=[0, 0, 105, 105], y=[69, -2, 69, -2])
    fig = px.scatter(x=[0, 0, 1, 1], y=[0, 1, 0, 1])
    fig.update_layout(xaxis=dict(range=[0, 1]))
    fig.update_layout(yaxis=dict(range=[0, 1]))
    fig.update_traces(marker=dict(color="white", size=6))

    # Remove side color scale and hide zero and gridlines
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        autosize=True
        # width=900,
        # height=600
    )

    # Disable axis ticks and labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    fig.update_layout(margin=dict(l=80, r=80, b=10, t=20))
    fig.update_layout(modebar=dict(bgcolor="rgba(0, 0, 0, 0)"))
    image_file = "assets/Pitch.png"
    image_path = os.path.join(os.getcwd(), image_file)

    # Import and use pre-fabricated football pitch image
    from PIL import Image

    img = Image.open(image_path)

    fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            sizing="stretch",
            opacity=0.7,
            layer="below",
        )
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=0.70)

    fig.update_layout(autosize=True)

    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(showgrid=False, showticklabels=False),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )
    return fig


def fig_from_json(filename):
    with open(filename, 'r',  encoding='utf-8') as f:
        fig = pio.from_json(f.read())
    return fig