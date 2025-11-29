import pandas as pd


EUROPE_REGIONS = {
        "Nordics": ["DK","SE","NO","FI","IS"],
        "Baltics": ["EE","LV","LT"],
        "Western Europe": ["FR","DE","BE","NL","LU","AT","CH","IE","GB"],
        "Southern Europe": ["IT","ES","PT","MT"],
        "Central Europe": ["PL","CZ","SK","HU","SI","HR"],
        "Balkans": ["RS","BA","ME","MK","AL","XK","BG","RO","TR","GR","CY"],
        "Eastern Europe": ["UA","MD","BY","RU"]
}

EUROPE_BLOCKS = {
    "West":["Nordics","Western Europe","Southern Europe"],
    "East":["Baltics","Central Europe","Balkans","Eastern Europe"]
}

COUNTRY_NAMES = {
    "FR":"France","DE":"Germany","BE":"Belgium","NL":"Netherlands","LU":"Luxembourg",
    "CH":"Switzerland","AT":"Austria","IE":"Ireland","GB":"United Kingdom",
    "DK":"Denmark","SE":"Sweden","NO":"Norway","FI":"Finland","IS":"Iceland",
    "EE":"Estonia","LV":"Latvia","LT":"Lithuania",
    "IT":"Italy","ES":"Spain","PT":"Portugal","GR":"Greece","CY":"Cyprus","MT":"Malta",
    "PL":"Poland","CZ":"Czech Republic","SK":"Slovakia","HU":"Hungary","SI":"Slovenia","HR":"Croatia",
    "RS":"Serbia","BG":"Bulgaria","RO":"Romania","BA":"Bosnia and Herzegovina",
    "ME":"Montenegro","MK":"North Macedonia","AL":"Albania","XK":"Kosovo",
    "TR":"Turkey","UA":"Ukraine","MD":"Moldova","BY":"Belarus","RU":"Russia"
}

EUROPE_REGION_COLORS = {
    "Nordics": "#1f77b4",        # blue
    "Baltics": "#9467bd",        # purple
    "Western Europe": "#2ca02c", # green
    "Southern Europe": "#ff7f0e",# orange
    "Central Europe": "#e377c2",  # pink
    "Balkans": "#8c564b",        # brown
    "Eastern Europe": "#d62728" # red 
}

SOURCE_COLOR_PALETTE = {
    "Coal": "#000000",      # Coal → black  
    "Oil": "#6E6E6E",     # Oil → dark grey  
    "Gas": "#1f77b4",      # Gas → blue  
    "Cement": "#C2B280",   # Cement → sand/stone  
    "Flaring": "#FF7F0E",  # Flaring → bright orange  
    "Other Industry": "#9467BD"  # Other → muted purple  
}

SOURCE_LABELS = {
    "Total Oil CO2 Emissions (Mt)": "Oil",
    "Total Coal CO2 Emissions (Mt)": "Coal",
    "Total Gas CO2 Emissions (Mt)": "Gas",
    "Total Cement CO2 Emissions (Mt)": "Cement",
    "Total Flaring CO2 Emissions (Mt)": "Flaring",
    "Total Other Industry CO2 Emissions (Mt)": "Other Industry"
}

SOURCE_COLOR_PALLETTE_BY_COL = {
    "Total Coal CO2 Emissions (Mt)": "#000000",      # Coal → black  
    "Total Oil CO2 Emissions (Mt)": "#6E6E6E",     # Oil → dark grey  
    "Total Gas CO2 Emissions (Mt)": "#1f77b4",      # Gas → blue  
    "Total Cement CO2 Emissions (Mt)": "#C2B280",   # Cement → sand/stone  
    "Total Flaring CO2 Emissions (Mt)": "#FF7F0E",  # Flaring → bright orange  
    "Total Other Industry CO2 Emissions (Mt)": "#9467BD"  # Other → muted purple  
}


def compute_subregion_summed_stats(df, metrics):
    rows = []
    # GROUP BY DATE FIRST
    for date, df_date in df.groupby("Year"):
        for region, codes in EUROPE_REGIONS.items():
            subset = df_date[df_date["Country_code"].isin(codes)]
            
            row = {
                "Country": region,
                "Year": date
            }
            
            for metric in metrics:
                row[metric] = subset[metric].sum(skipna=True)
                
            rows.append(row)

    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

def compute_block_summed_stats(df, metrics):
    rows = []
    # GROUP BY DATE FIRST
    for date, df_date in df.groupby("Year"):
        for block, regions in EUROPE_BLOCKS.items():
            
            # Flatten regions into country codes
            codes = [c for r in regions for c in EUROPE_REGIONS[r]]
            subset = df_date[df_date["Country_code"].isin(codes)]
            
            row = {
                "Country": block,
                "Year": date
            }
            
            for metric in metrics:
                row[metric] = subset[metric].sum(skipna=True)
                
            rows.append(row)

    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)


def get_europe_data(eu_df):
    # Last reported row per country
    eu_latest = eu_df.sort_values("Year").groupby("Country").tail(1)

    EU_CENTROIDS_2 = {
        "AL": (41.1533, 20.1683),
        "AD": (42.5063, 1.5218),
        "AT": (47.5162, 14.5501),
        "BY": (53.7098, 27.9534),
        "BE": (50.5039, 4.4699),
        "BA": (43.9159, 17.6791),
        "BG": (42.7339, 25.4858),
        "HR": (45.1000, 15.2000),
        "CY": (35.1264, 33.4299),
        "CZ": (49.8175, 15.4730),
        "DK": (56.2639, 9.5018),
        "EE": (58.5953, 25.0136),
        "FI": (61.9241, 25.7482),
        "FR": (46.2276, 2.2137),
        "DE": (51.1657, 10.4515),
        "GR": (39.0742, 21.8243),
        "HU": (47.1625, 19.5033),
        "IS": (64.9631, -19.0208),
        "IE": (53.1424, -7.6921),
        "IT": (41.8719, 12.5674),
        "LV": (56.8796, 24.6032),
        "LI": (47.1660, 9.5554),
        "LT": (55.1694, 23.8813),
        "LU": (49.8153, 6.1296),
        "MT": (35.9375, 14.3754),
        "MD": (47.4116, 28.3699),
        "MC": (43.7384, 7.4246),
        "ME": (42.7087, 19.3744),
        "NL": (52.1326, 5.2913),
        "MK": (41.6086, 21.7453),
        "NO": (60.4720, 8.4689),
        "PL": (51.9194, 19.1451),
        "PT": (39.3999, -8.2245),
        "RO": (45.9432, 24.9668),
        "RU": (55.75, 37.62),     # <- placed in European Russia (Moscow)
        "SM": (43.9424, 12.4578),
        "RS": (44.0165, 21.0059),
        "SK": (48.6690, 19.6990),
        "SI": (46.1512, 14.9955),
        "ES": (40.4637, -3.7492),
        "SE": (60.1282, 18.6435),
        "CH": (46.8182, 8.2275),
        "UA": (48.3794, 31.1656),
        "GB": (55.3781, -3.4360),
        "TR": (39.9334, 32.8597)   # Ankara
    }

    eu_latest["lat"] = eu_latest["Country_code"].map(lambda c: EU_CENTROIDS_2.get(c, (None, None))[0])
    eu_latest["lon"] = eu_latest["Country_code"].map(lambda c: EU_CENTROIDS_2.get(c, (None, None))[1])

    def assign_region(code):
        for region, codes in EUROPE_REGIONS.items():
            if code in codes:
                return region
        return None  # for safety
    
    eu_latest["Region"] = eu_latest["Country_code"].apply(assign_region)

    return eu_latest

def get_europe_data_OWID(df):
    eu = df[df["country"].isin(COUNTRY_NAMES.values())][["country","year","co2","population","gdp","coal_co2", "oil_co2", "gas_co2", "cement_co2", "flaring_co2", "other_industry_co2"]]
    # Rename columns
    eu.rename(columns={
        "country": "Country",
        "year": "Year",
        "co2": "CO2 Emissions (Mt)",
        "population": "Population",
        "gdp": "GDP ($)",
        "coal_co2": "Coal CO2 Emissions (Mt)",
        "oil_co2": "Oil CO2 Emissions (Mt)",
        "gas_co2": "Gas CO2 Emissions (Mt)",
        "cement_co2": "Cement CO2 Emissions (Mt)",
        "flaring_co2": "Flaring CO2 Emissions (Mt)",
        "other_industry_co2": "Other Industry CO2 Emissions (Mt)"
    }, inplace=True)

    eu["CO2 Emissions (kg)"] = eu["CO2 Emissions (Mt)"]*1_000_000 *1_000 # Convert from Mt to kg

    eu["Country_code"] = eu["Country"].map({v: k for k, v in COUNTRY_NAMES.items()})
    

    eu = compute_subregion_summed_stats(eu, ["CO2 Emissions (kg)", "Population", "GDP ($)", "Coal CO2 Emissions (Mt)", "Oil CO2 Emissions (Mt)", "Gas CO2 Emissions (Mt)", "Cement CO2 Emissions (Mt)", "Flaring CO2 Emissions (Mt)", "Other Industry CO2 Emissions (Mt)"])
    eu = compute_block_summed_stats(eu, ["CO2 Emissions (kg)", "Population", "GDP ($)", "Coal CO2 Emissions (Mt)", "Oil CO2 Emissions (Mt)", "Gas CO2 Emissions (Mt)", "Cement CO2 Emissions (Mt)", "Flaring CO2 Emissions (Mt)", "Other Industry CO2 Emissions (Mt)"])
    eu["CO2 Emissions / GDP (kg/$)"] = eu["CO2 Emissions (kg)"] / eu["GDP ($)"]

    agg = eu.groupby("Country").agg(
        total_co2_emissions=("CO2 Emissions (kg)", "sum"),
        total_co2_emissions_per_gdp=("CO2 Emissions / GDP (kg/$)", "sum"),
        total_coal_co2_emissions=("Coal CO2 Emissions (Mt)", "sum"),
        total_oil_co2_emissions=("Oil CO2 Emissions (Mt)", "sum"),
        total_gas_co2_emissions=("Gas CO2 Emissions (Mt)", "sum"),
        total_cement_co2_emissions=("Cement CO2 Emissions (Mt)", "sum"),
        total_flaring_co2_emissions=("Flaring CO2 Emissions (Mt)", "sum"),
        total_other_industry_co2_emissions=("Other Industry CO2 Emissions (Mt)", "sum"),
    ).reset_index()
    agg.rename(columns={
        "total_co2_emissions": "Total CO2 Emissions (kg)",
        "total_co2_emissions_per_gdp": "Total CO2 Emissions / GDP (kg/$)",
        "total_coal_co2_emissions": "Total Coal CO2 Emissions (Mt)",
        "total_oil_co2_emissions": "Total Oil CO2 Emissions (Mt)",
        "total_gas_co2_emissions": "Total Gas CO2 Emissions (Mt)",
        "total_cement_co2_emissions": "Total Cement CO2 Emissions (Mt)",
        "total_flaring_co2_emissions": "Total Flaring CO2 Emissions (Mt)",
        "total_other_industry_co2_emissions": "Total Other Industry CO2 Emissions (Mt)"
    }, inplace=True)

    eu = eu.merge(agg, on="Country", how="left")

    return get_europe_data(eu)