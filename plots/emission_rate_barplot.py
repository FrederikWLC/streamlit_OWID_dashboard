import seaborn as sns
import matplotlib.pyplot as plt
from data.europe import EUROPE_REGIONS, EUROPE_BLOCKS

def emission_rate_block_barplot_figure(df):

    blocks_df = df[df["Country"].isin(EUROPE_BLOCKS.keys())][["Country", "Total CO2 Emissions / GDP (kg/$)"]]
    blocks_df = blocks_df.sort_values("Total CO2 Emissions / GDP (kg/$)", ascending=True)

    plt.figure(figsize=(5, 6))
    sns.barplot(
        data=blocks_df,
        x="Country",
        y="Total CO2 Emissions / GDP (kg/$)",
        palette="YlOrBr"
    )

    plt.title("Total CO2 Emissions / GDP by East/West Divide")
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return plt.gcf()

def emission_rate_subregion_barplot_figure(df):

    subregions_df = df[df["Country"].isin(EUROPE_REGIONS.keys())][["Country", "Total CO2 Emissions / GDP (kg/$)"]]
    subregions_df = subregions_df.sort_values("Total CO2 Emissions / GDP (kg/$)", ascending=True)

    plt.figure(figsize=(5, 6.5))
    sns.barplot(
        data=subregions_df,
        x="Total CO2 Emissions / GDP (kg/$)",
        y="Country",
        palette="YlOrBr"
    )

    plt.title("Total CO2 Emissions / GDP by European Subregions")
    plt.ylabel("")
    plt.tight_layout()

    return plt.gcf()
