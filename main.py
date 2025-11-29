import streamlit as st
import pandas as pd

from plots import (
    emission_rate_figure,
    emission_rate_block_barplot_figure,
    emission_rate_subregion_barplot_figure,
    industry_share_block_figure,
    industry_share_subregion_barplot_figure,
    industry_share_map_figure,
    subregions_figure
)

from data.europe import (
    get_europe_data_OWID,
    EUROPE_REGIONS,
    COUNTRY_NAMES,
    EUROPE_REGION_COLORS
)

from icons import flag_svg


st.set_page_config(
    page_title="European CO2 Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
            
    /* remove vertical padding BETWEEN streamlit columns */
    div[data-testid="column"] > div:nth-child(1) {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* remove bottom padding inside those column containers */
    div[data-testid="column"] > div {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
            

    h1 {
        margin-top: 0px !important;
        padding-top: 0px !important;
    }

    div.block-container {
        padding-top: 20px !important;
        margin-top: 0 !important;
    }  

    /* Remove Streamlit default header */
    header {visibility: hidden;}
    header {height: 0px;}  

    /* prevent Streamlit from generating <div class='arrow-bar'></div> */
    .arrow-bar-btnrow { 
        display: flex;
        gap: 0px;
        margin-top: 0px;
        margin-bottom: 16px;
        height: 46px;
    }

    .stButton > button {
        width: 100%;
        height: 46px !important;
        border: none !important;
        font-weight: 600;
        color: #1d1d1d !important;
        background: #e8ecf3 !important;
        cursor: pointer;
        padding-left: 28px;
        padding-right: 45px;
        clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%);
        transition: background 0.12s ease;
    }

    .stButton > button:disabled {
        background: #12436D !important;
        color: white !important;
        cursor: default !important;
        border: 2px solid #1059a3 !important;
    }

    .stButton > button:hover:enabled {
        background: #d4d9e3 !important;
    }

    .stButton > button:active {
        cursor: progress !important;
    }
    </style>
""", unsafe_allow_html=True)
# CACHING
@st.cache_data
def load_raw():
    df_OWID = pd.read_csv(
        "owid-co2-data-interpolated.csv",
        parse_dates=["year"]
    )
    return df_OWID

@st.cache_data
def prep_OWID(df):
    return get_europe_data_OWID(df[df["year"] >= "1990"])


df_OWID = load_raw()
df_OWID_europe = prep_OWID(df_OWID)


if "page" not in st.session_state:
    st.session_state.page = "page1"

# Start of displays
html_header = """
<div style='display:flex; align-items:center; gap:14px; margin-bottom:10px; margin-top:-5px;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/4/44/Our_World_in_Data_logo.png' style='height:40px; width:auto;'>
    <div style='font-size:22px; font-weight:600; line-height:1.1;'>
        East/West Divide in European CO2 Emissions (1990-2023)<br>
        <span style='font-size:16px; font-weight:400; color:gray;'>An analysis of CO2 emissions and industries using OWID data</span>
    </div>
</div>
"""

st.markdown(html_header, unsafe_allow_html=True)

pages = {
    "page1": "What? - Emissions / GDP higher in the East",
    "page2": "Really? - Coal is the culprit",
    "page3": "So what? - Let's paint it green"
}


arrow_container = st.container()

with arrow_container:

    st.markdown("<div class='arrow-bar'>", unsafe_allow_html=True)

    cols = st.columns(len(pages))

    for i, (key, label) in enumerate(pages.items()):
        is_selected = (st.session_state.page == key)

        with cols[i]:
            if st.button(label, key=f"btn_{key}", disabled=is_selected, use_container_width=True):
                st.session_state.page = key
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


page_container = st.container()


# PAGE 1 — WHAT?  (Lethality)
with page_container:
    if st.session_state.page == "page1":


        st.title("While the Western parts of Europe have had more total emissions, the Eastern countries emit more than twice as much per unit of GDP")


        col_block, col_map, col_sub,  = st.columns([1, 1.3, 1])


        with col_block:
            st.pyplot(emission_rate_block_barplot_figure(df_OWID_europe))

        with col_map:
            st.plotly_chart(
                emission_rate_figure(df_OWID_europe),
                use_container_width=False,
                config={"displayModeBar": False}
            )
            st.markdown("""<p style='text-align: center;margin-left: 20px;margin-right: 20px;'>Note: GDP is measured in international-$ at 2021 prices to account for inflation and differences in living costs
            between countries.</p>""", unsafe_allow_html=True)


        with col_sub:
            st.pyplot(emission_rate_subregion_barplot_figure(df_OWID_europe))


        with st.expander("See region definitions", expanded=False):

            st.subheader("European Subregions")

            left_defs, right_map = st.columns([2, 1])

            with left_defs:
                for region, codes in EUROPE_REGIONS.items():
                    flags = "".join(flag_svg(c, COUNTRY_NAMES[c], size=20) for c in codes)
                    dot = EUROPE_REGION_COLORS[region] + "CC"
                    st.markdown(
                        f"""
                        <div style='margin-bottom:6px;'>
                            <b style='color:{dot};'>●</b> 
                            <b>{region}:</b> {flags}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with right_map:
                region_map_df = pd.DataFrame(
                    [(COUNTRY_NAMES[c], r)
                        for r, codes in EUROPE_REGIONS.items()
                        for c in codes],
                    columns=["Country", "Region"]
                )

                st.plotly_chart(
                    subregions_figure(region_map_df, EUROPE_REGION_COLORS),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )
    
# PAGE 2 — REALLY? (Underreporting)
    elif st.session_state.page == "page2":

        st.title("Heavy reliance on coal in the East is a major factor behind their higher CO₂ emissions per unit of GDP compared to the West")

        col_block, col_map, col_sub = st.columns([1, 1, 1])

        with col_block:
            st.plotly_chart(industry_share_block_figure(df_OWID_europe))

        with col_map:
            st.plotly_chart(
                industry_share_map_figure(df_OWID_europe),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        with col_sub:
            st.pyplot(industry_share_subregion_barplot_figure(df_OWID_europe))
        
        st.markdown("""<p style="font-size:22px;">Coal emits about 2-3 times as much CO₂ per euro produced compared to natural gas or oil. Central European countries in particular continue to depend heavily on coal for both power and industry, which makes their economies especially carbon intensive. In the East, Russia and other countries in its subregion rely more on natural gas, yet still emit far more CO₂ per euro produced than the West. Western countries have generally transitioned earlier toward cleaner energy sources and more service-based economies. As a result, Central Europe stands out as the region where coal dependence drives the strongest mismatch between economic output and emissions.</p>""", unsafe_allow_html=True)


# PAGE 3 — SO WHAT?
    elif st.session_state.page == "page3":
        col1, col2 = st.columns([1,1])
        with col1:
            st.image("https://acclaimenergy.com/wp-content/uploads/2023/02/energy-consulting.jpeg", use_container_width=True)
        with col2:
            st.title("Accelerating The Central and Eastern European Energy Transition")
            st.markdown("""
                <div style='font-size:22px; line-height:1.55;'>
                Western European industries and policymakers can play a constructive role in supporting Central Europe and the broader East in reducing coal dependence and lowering carbon intensity. Many Central European economies still rely on older coal-based infrastructure, making their production especially emission-heavy, while Russia and its neighboring Eastern subregion remain centered on natural gas. Through targeted collaboration — such as modernizing power systems, expanding grid interconnections, and helping industry adopt cleaner technologies — Western partners can help unlock more efficient and lower-carbon growth. The objective is not to replace domestic capabilities, but to build on them, enabling these regions to generate the same economic value with far fewer emissions, strengthening energy security and sustainability across all of Europe. </div>
            """, unsafe_allow_html=True)