import plotly.express as px

def subregions_figure(region_map_df, region_colors):

    def soften(hex_color, alpha=0.55):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    soft_region_colors = {region: soften(color,0.55) for region, color in region_colors.items()}

    fig_regions = px.choropleth(
        region_map_df,
        locations="Country",
        locationmode="country names",
        color="Region",
        color_discrete_map=soft_region_colors,
        projection="natural earth"
    )

    fig_regions.update_geos(
        lataxis_range=[34, 72],
        lonaxis_range=[-18, 38],
        resolution=110,
        landcolor="gray",
        oceancolor="#0e1117",
        bgcolor="#0e1117",
        showcoastlines=False,
        showcountries=False,
        showland=True)

    fig_regions.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        showlegend=False,
        coloraxis_showscale=False
    )

    return fig_regions
