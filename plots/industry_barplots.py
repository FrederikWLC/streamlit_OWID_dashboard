import plotly.express as px
from data.europe import EUROPE_BLOCKS, EUROPE_REGIONS, SOURCE_COLOR_PALETTE, SOURCE_LABELS
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

def industry_share_block_figure(df):

    df_blocks = df[df["Country"].isin(EUROPE_BLOCKS.keys())].copy()

    df_blocks.rename(columns={"Country": "Block"}, inplace=True)

    df_blocks = df_blocks[list(SOURCE_LABELS.keys()) + ["Block"]].sort_values(
        by=list(SOURCE_LABELS.keys()),
        ascending=False
    )


    numeric_cols = list(SOURCE_LABELS.keys())

    # compute shares
    shares = df_blocks.copy()
    shares[numeric_cols] = df_blocks[numeric_cols].div(
        df_blocks[numeric_cols].sum(axis=1),
        axis=0
    )

    # compute total emissions per country
    total_by_country = (
        df_blocks
        .set_index("Block")[numeric_cols]
        .sum(axis=1)
    )

    df_plot = shares.reset_index().melt(
        id_vars="Block",
        var_name="Industry",
        value_name="Share"
    )

    df_plot["Industry"] = df_plot["Industry"].map(SOURCE_LABELS)

    # FIX: correct mapping
    df_plot["Total Emissions (Mt)"] = df_plot["Block"].map(total_by_country)

    df_plot["CO2 Emissions (Mt)"] = df_plot["Share"] * df_plot["Total Emissions (Mt)"]
    df_plot = df_plot[["Block", "Industry", "Share", "CO2 Emissions (Mt)"]]

    fig = px.bar(
        df_plot,
        x="Block",
        y="CO2 Emissions (Mt)",
        color="Industry",
        color_discrete_map=SOURCE_COLOR_PALETTE,
        barmode="stack",
        title="CO₂ Sources - East vs West",
        hover_data={"Share": ":.1%", "CO2 Emissions (Mt)": ":.1f"},
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        title=dict(font=dict(color="black"),x=0.5,
        xanchor="center"),

        xaxis=dict(
            tickfont=dict(color="black"),
            title=dict(font=dict(color="black"))
        ),
        yaxis=dict(
            tickfont=dict(color="black"),
            title=dict(font=dict(color="black"))
        ),
        height=550,
        width=800,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis_title="",
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.1,
            xanchor="center",
            bgcolor="rgba(255,255,255,0)",
            font=dict(color="black"),
            title=dict(font=dict(color="black"))
        ),
        showlegend=False

    )

    return fig


def industry_share_subregion_barplot_figure(df):

    df = df.copy()
    df = df[df["Year"] == df["Year"].max()]

    df_subregions = df[df["Country"].isin(EUROPE_REGIONS.keys())]
    

    totals = df_subregions.groupby("Country")[list(SOURCE_LABELS.keys())].sum()
    shares = totals.div(totals.sum(axis=1), axis=0)

    df_plot = shares.reset_index().melt(
        id_vars="Country",
        var_name="Industry",
        value_name="Share"
    )
    df_plot["Industry"] = df_plot["Industry"].map(SOURCE_LABELS)

    plt.figure(figsize=(7, 7))
    sns.barplot(
        data=df_plot,
        x="Share",
        y="Country",
        hue="Industry",
        palette=SOURCE_COLOR_PALETTE,
        orient="h")

    plt.title("Industry Share of Total CO₂ - European Subregions")
    plt.xlabel("Share")
    plt.ylabel("")
    plt.legend(title="Industry")
    plt.tight_layout()
    plt.legend([], [], frameon=False)

    return plt.gcf()
