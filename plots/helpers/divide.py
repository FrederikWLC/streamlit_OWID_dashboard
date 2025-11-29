import plotly.graph_objects as go

def add_east_west_divide_lines(fig):
    east_west_border_lon = [
            14.3,  # DE/PL Baltic area
            14.6,  # Szczecin area
            15.0,  # Görlitz
            13.8,  # Smooth Czech west bulge (Cheb-ish)
            14.8,  # South Czech border toward AT
            16.4,  # Vienna east border
            16.0,  # Graz region, still east of AT
            13.6,  # Slovenia east boundary shift (Ljubljana stays east)
            13.5   # Adriatic, further east → Slovenia clearly east
        ]

    east_west_border_lat = [
        53.7,
        53.3,
        51.1,
        50.1,
        48.7,
        48.2,
        46.8,
        46.3,
        45.8
    ]


    fi_ru_border_lon = [
        28.5,  # Gulf of Finland
        28.6,  # Vyborg area
        29.3,  # Lake Ladoga
        29.9,  # Ladoga-Karelia
        30.0,  # N. Karelia
        29.2,  # Kainuu
        28.7,  # Taiga
        29.4,  # Lapland
        29.1,  # Border corridor to Norway
        30.6   # Barents Sea (north of Kirkenes)
    ]

    fi_ru_border_lat = [
        60.6,
        61.0,
        61.8,
        62.7,
        63.8,
        64.8,
        66.0,
        67.3,
        68.8,
        69.8   # Arctic ocean continuation
    ]


    east_west_divide_lon = (
    east_west_border_lon
    + [None] 
    + fi_ru_border_lon
    )

    east_west_divide_lat = (
        east_west_border_lat
        + [None]
        + fi_ru_border_lat
    )

    fig.add_trace(go.Scattergeo(
        lon=east_west_divide_lon,
        lat=east_west_divide_lat,
        mode="lines",
        line=dict(color="black", width=3, dash="dashdot"),
        hoverinfo="skip",
        showlegend=True,
        name="East / West Divide (Historical Cultural Spheres)"
    ))