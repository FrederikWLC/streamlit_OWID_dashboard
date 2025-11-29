import plotly.express as px
from plots.helpers.divide import add_east_west_divide_lines
from data.europe import EUROPE_REGIONS, EUROPE_BLOCKS, SOURCE_LABELS, SOURCE_COLOR_PALETTE
from plotly import graph_objects as go


def industry_share_map_figure(df):
    df = df.copy()
    df = df[df["Year"] == df["Year"].max()]

    df_countries = df[
        ~(df["Country"].isin(EUROPE_REGIONS.keys()) |
            df["Country"].isin(EUROPE_BLOCKS.keys()))
    ].copy()


    df_countries["Dominant Industry"] = (
    df_countries[list(SOURCE_LABELS.keys())]
    .idxmax(axis=1)
    .replace(SOURCE_LABELS)
    )

    industry_cols = list(SOURCE_LABELS.keys())

    sorted_cols = df_countries[industry_cols].apply(
        lambda row: row.sort_values(ascending=False).index.tolist(),
        axis=1
    )

    df_countries["2nd Dominant Industry"] = (
        sorted_cols.str[1].replace(SOURCE_LABELS)
    )

    df_countries["3rd Dominant Industry"] = (
        sorted_cols.str[2].replace(SOURCE_LABELS)
    )

    df_filtered = df_countries[["Country", "lon", "lat", "Dominant Industry", "2nd Dominant Industry", "3rd Dominant Industry"]]
    fig = px.scatter_geo(df_filtered, lon="lon", lat="lat",
                     color="Dominant Industry",
                     color_discrete_map=SOURCE_COLOR_PALETTE,
                     hover_name="Country",title="Biggest CO₂ Industry Source by Country in Europe")


    fig.update_geos(
        lataxis_range=[30,80],
        lonaxis_range=[-20,45],
        resolution=110,
        fitbounds=None
    )

    fig.update_traces(
        hoverinfo="skip",
        hovertemplate=None,
        marker=dict(size=20),
    )

    add_east_west_divide_lines(fig)

    fig.update_layout(
        height=550,
        width=800,
        margin=dict(l=0,r=0,t=40,b=0),
        legend=dict(
            orientation="v",
            x=0.1,
            y=0.98,
            xanchor="left",
            bgcolor="rgba(255,255,255,0.75)",
            font=dict(color="black", size=14),
            title=dict(font=dict(color="black", size=16))
        ),
        showlegend=True,
        title=dict(x=0.5, xanchor="center", font=dict(color="white"))
    )

    for label, color in SOURCE_COLOR_PALETTE.items():
        if label in ["Coal", "Oil", "Gas"]:
            fig.add_trace(
                go.Scattergeo(
                    lon=[None], lat=[None],        # won't draw on map
                    mode="markers",
                    marker=dict(size=12, color=color),
                    name=label,                    # FIX: legend entry per category
                    showlegend=True
                )
            )

    for i in range(3):
        fig.data[i].showlegend = False

    return fig