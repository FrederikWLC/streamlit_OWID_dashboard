import plotly.express as px
from plots.helpers.divide import add_east_west_divide_lines
from data.europe import EUROPE_BLOCKS, EUROPE_REGIONS

def emission_rate_figure(df):

    df_filtered = df[~(df["Country"].isin(EUROPE_BLOCKS.keys()) | df["Country"].isin(EUROPE_REGIONS.keys()))]

    fig = px.scatter_geo(
        df_filtered,
        lon= "lon",
        lat= "lat",
        color="Total CO2 Emissions / GDP (kg/$)",
        size="Total CO2 Emissions (kg)",
        hover_name="Country",
        projection="natural earth",
        color_continuous_scale="YlOrBr",
        size_max=40    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "<b>Total CO2 Emissions:</b> %{customdata[0]:,.0f} kg<br>"
            "<b>Population:</b> %{customdata[1]:,.0f}<br>"
            "<b>GDP:</b> %{customdata[2]:,.0f} $<br>"
            "<b>CO2 Emissions / GDP:</b> %{customdata[3]:.1f} kg/$"
            "<extra></extra>"
        ),
        customdata=df_filtered[[
            "Total CO2 Emissions (kg)",
            "Population",
            "GDP ($)",
            "Total CO2 Emissions / GDP (kg/$)"
        ]]
        )

    add_east_west_divide_lines(fig)

    fig.update_geos(
        lataxis_range=[34, 72],
        lonaxis_range=[-15, 40],
        resolution=110,
        fitbounds=None
    )

    fig.update_layout(
        height=550,
        width=800,
        margin=dict(l=0, r=0, t=0, b=0),   

        legend=dict(
            orientation="h",
            x=0.1,
            y=0.87,                
            xanchor="left",
            yanchor="bottom",
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="black", size=14)
        ),

        coloraxis_colorbar=dict(
            orientation="h",
            x=0.5,
            y=1.1,               
            xanchor="center",
            yanchor="top",
            thickness=14,
            len=0.85,
            title_side="top",
            title="CO2 Emissions / GDP (kg/$)",
        ),

        annotations=[dict(
            x=0.1,
            y=0.90,                     
            xref="paper",
            yref="paper",
            text="Bubble size = Total emissions",
            showarrow=False,
            font=dict(size=14, color="orange")
        )]
    )

    fig.update_layout(autosize=False)

    return fig
