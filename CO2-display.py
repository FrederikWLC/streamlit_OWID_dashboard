from plots.excess_death_rate_plot import excess_death_rate_figure
import streamlit as st
import pandas as pd
from plots import death_rate_figure, death_block_barplot_figure, death_subregion_barplot_figure, subregions_figure, excess_death_block_barplot_figure, excess_death_subregion_barplot_figure
from data.europe import get_europe_data_WHO, get_europe_data_OWID, get_merged_europe_data, EUROPE_REGIONS, COUNTRY_NAMES, EUROPE_REGION_COLORS
from icons import flag_svg


df_WHO = pd.read_csv('WHO-COVID-19-global-daily-data-clean.csv')
df_OWID = pd.read_csv('https://catalog.ourworldindata.org/garden/excess_mortality/latest/excess_mortality/excess_mortality.csv')
df_WHO_europe = get_europe_data_WHO(df_WHO)
df_OWID_europe = get_europe_data_OWID(df_OWID)

# Start of Display
st.title("While Western Europe had more absolute cases, Eastern Europe and the Balkans showed higher lethality")
fig1 = death_rate_figure(df_WHO_europe)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Regional Differences in Lethality")
col1, col2 = st.columns(2)
with col1:
    fig2 = death_block_barplot_figure(df_WHO_europe)
    st.pyplot(fig2)
with col2:
    fig3 = death_subregion_barplot_figure(df_WHO_europe)
    st.pyplot(fig3)

with st.expander("See region definitions"):

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("European Subregions (Used in the Dashboard)")

        for region, codes in EUROPE_REGIONS.items():
            flags_html = "".join(flag_svg(code, COUNTRY_NAMES[code], size=18) for code in codes)

            # matte circle (not huge square)
            color = EUROPE_REGION_COLORS[region] + "CC"  # add transparency for elegance
            dot = f"<span style='display:inline-block; width:10px; height:10px; background:{color}; border-radius:50%; margin-right:8px;'></span>"

            st.markdown(
                f"""
                <div style='display:flex; align-items:center; margin-bottom:10px;'>
                    {dot}
                    <b>{region}:</b>&nbsp; {flags_html}
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        region_map_df = pd.DataFrame(
            [(COUNTRY_NAMES[code], region)
            for region, codes in EUROPE_REGIONS.items()
            for code in codes],
            columns=["Country", "Region"]
        )
        region_map_df["Region"] = region_map_df["Region"].astype("category")

        st.plotly_chart(
            subregions_figure(region_map_df, EUROPE_REGION_COLORS),
            use_container_width=True
        )

df_merged_europe = get_merged_europe_data(df_WHO, df_OWID)
st.title("Larger amounts of Non-COVID Excess Deaths Indicate Underreporting in Eastern Europe")
fig4 = excess_death_rate_figure(df_merged_europe)
st.plotly_chart(fig4, use_container_width=True)


st.subheader("Regional Differences in Non-COVID Excess Deaths")
col1, col2 = st.columns(2)
with col1:
    fig5 = excess_death_block_barplot_figure(df_merged_europe)
    st.pyplot(fig5)
with col2:
    fig6 = excess_death_subregion_barplot_figure(df_merged_europe)
    st.pyplot(fig6)