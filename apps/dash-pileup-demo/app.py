import os
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bio
import pandas as pd
import numpy as np
import math

from layout_helper import run_standalone_app

text_style = {"color": "#506784", "font-family": "Open Sans"}

_COMPONENT_ID = "pileup-browser"

def description():
    return "An interactive in-browser track viewer."


def azure_url(file):
    return os.path.join("https://sampleappsdata.blob.core.windows.net/dash-pileup-demo/rna/", file)


def header_colors():
    return {
        "bg_color": "#0F5BA7",
        "font_color": "white",
    }


def rna_differential(app):

    basal_lactate = {
        "url": azure_url("SRR1552454.fastq.gz.sampled.bam"),
        "indexUrl": azure_url("SRR1552454.fastq.gz.sampled.bam.bai"),
    }

    luminal_lactate = {
        "url": azure_url("SRR1552448.fastq.gz.sampled.bam"),
        "indexUrl": azure_url("SRR1552448.fastq.gz.sampled.bam.bai"),
    }

    HOSTED_TRACKS = {
        'range': {"contig": "chr1", "start": 54986297, "stop": 54991347},
        'celltype': [
            {"viz": "scale", "label": "Scale"},
            {"viz": "location", "label": "Location"},
            {
                "viz": "genes",
                "label": "genes",
                "source": "bigBed",
                "sourceOptions": {
                    "url":  azure_url("mm10.ncbiRefSeq.sorted.bb")
                },
            },
            {
                "viz": "coverage",
                "label": "Basal",
                "source": "bam",
                "sourceOptions": basal_lactate,
            },
            {
                "viz": "pileup",
                "vizOptions": {"viewAsPairs": True},
                "label": "Basal",
                "source": "bam",
                "sourceOptions": basal_lactate,
            },
            {
                "viz": "coverage",
                "label": "Luminal",
                "source": "bam",
                "sourceOptions": luminal_lactate,
            },
            {
                "viz": "pileup",
                "label": "Luminal",
                "source": "bam",
                "sourceOptions": luminal_lactate,
            },
        ]
    }

    return HOSTED_TRACKS


REFERENCE = {
    "label": "mm10",
    "url": "https://hgdownload.cse.ucsc.edu/goldenPath/mm10/bigZips/mm10.2bit",
}

DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/data")

# Differentially expressed genes (identified in R, see assets/data/rna/README.md)
DE_dataframe = pd.read_csv(azure_url("DE_genes.csv"))
# filter for the cell type condition
DE_dataframe = DE_dataframe[DE_dataframe['Comparison'] == "luminal__v__basal"].reset_index()

# add SNP column
DE_dataframe["SNP"] = "NA"


# get min and max effect sizes
df_min = math.floor(min(DE_dataframe['log2FoldChange']))
df_max = math.ceil(max(DE_dataframe['log2FoldChange']))


def layout(app):
    HOSTED_CASE_DICT = rna_differential(app)

    return html.Div(
        id="pileup-body",
        className="app-body",
        children=[
            html.Div(
                id="pileup-control-tabs",
                className="control-tabs",
                children=[
                    dcc.Tabs(
                        id="pileup-tabs",
                        value="data",
                        children=[
                            dcc.Tab(
                                label="Data",
                                value="data",
                                children=html.Div(
                                    className="control-tab",
                                    children=[
                                        'Effect Size',
                                        dcc.RangeSlider(
                                            id='pileup-volcanoplot-input',
                                            min=df_min,
                                            max=df_max,
                                            step=None,
                                            marks={
                                                i: {'label': str(i)} for i in range(df_min, df_max+1, 2)
                                            },
                                            value=[-1,1]
                                        ),
                                        html.Br(),
                                        dcc.Graph(
                                            id="pileup-dashbio-volcanoplot",
                                            figure=dash_bio.VolcanoPlot(
                                                dataframe=DE_dataframe,
                                                effect_size="log2FoldChange",
                                                effect_size_line = [-1,1],
                                                title="Differentially Expressed Genes",
                                                genomewideline_value=-np.log10(0.05),
                                                p="padj",
                                                snp="SNP",
                                                gene="Gene",
                                            ),
                                        )
                                    ],
                                ),
                            ),
                            dcc.Tab(
                                label="About",
                                value="what-is",
                                children=html.Div(
                                    className="control-tab",
                                    children=[
                                        html.H4(
                                            className="what-is",
                                            children="What is pileup.js?",
                                        ),
                                        dcc.Markdown(
                                            """
                                The Dash pileup.js component is a high-performance genomics
                                data visualization component developed originally by the Hammer Lab
                                (https://github.com/hammerlab/pileup.js). pileup.js
                                supports visualization of genomic file formats, such as vcfs,
                                bam, and bigbed files. pileup.js additionally allows flexible
                                interaction with non-standard data formats. Users can visualize
                                GA4GH JSON formatted alignments, features and variants. Users can
                                also connect with and visualize data stored in GA4GH formatted data
                                stores.
                                """
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    )
                ],
            ),
            dcc.Loading(
                parent_className="dashbio-loading",
                id="pileup-output",
                children=html.Div(
                    [
                        dash_bio.Pileup(
                            id=_COMPONENT_ID,
                            range=HOSTED_CASE_DICT["range"],
                            reference=REFERENCE,
                            tracks=HOSTED_CASE_DICT["celltype"],
                        )
                    ]
                ),
            ),
        ],
    )


def callbacks(_app):
    HOSTED_CASE_DICT = rna_differential(_app)

    @_app.callback(
        Output('pileup-dashbio-volcanoplot', 'figure'),
        [Input('pileup-volcanoplot-input', 'value')]
    )
    def update_volcano(effects):

        return dash_bio.VolcanoPlot(
            dataframe=DE_dataframe,
            effect_size='log2FoldChange',
            effect_size_line=effects,
            title="Differentially Expressed Genes",
            genomewideline_value=-np.log10(0.05),
            p='padj',
            snp='SNP',
            gene='Gene',
        )

    @_app.callback(
        Output(_COMPONENT_ID, "range"),
        Input("pileup-dashbio-volcanoplot", "clickData")
    )
    def update_range(point):

        if point is None:
            range = HOSTED_CASE_DICT["range"]
        else:

            # get genomic location of selected genes and goto
            pointText = point["points"][0]["text"]
            gene = pointText.split("GENE: ")[-1]

            row = DE_dataframe[DE_dataframe["Gene"] == gene].iloc[0]

            range = {"contig": row["chr"], "start": row["start"], "stop": row["end"]}

        return range


app = run_standalone_app(layout, callbacks, header_colors, __file__)
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
