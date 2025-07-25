import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import requests
from urllib.error import URLError


@st.cache_data
def fetch_covid():
    url = "https://disease.sh/v3/covid-19/countries"
    r = requests.get(url)
    if r.status_code != 200:
        st.error(f"API request failed with status code {r.status_code}")
        return pd.DataFrame()
    data = r.json()
    rows = []
    for country in data:
        cases = country.get("cases")
        name = country.get("country")
        coord = country.get("countryInfo", {})
        lat = coord.get("lat")
        lng = coord.get("long")
        if lat is not None and lng is not None and cases is not None:
            rows.append({
                "location": name,
                "cases": cases,
                "latitude": lat,
                "longitude": lng,
            })
    df = pd.DataFrame(rows)

    # Normalize radius from 100 to 100000
    min_cases = df["cases"].min()
    max_cases = df["cases"].max()
    df["radius"] = 100 + (df["cases"] - min_cases) / (max_cases - min_cases) * (1000000 - 200000)

    return df


try:
    df = fetch_covid()

    if df.empty:
        st.error("No data to display.")
    else:
        st.title("🌍 Global COVID Map with Arcs and Scaled Bubbles")
        sidebar = st.sidebar
        show_bubbles = sidebar.checkbox("Show red case bubbles", True)
        show_labels = sidebar.checkbox("Show country names", True)
        show_arcs = sidebar.checkbox("Show jumping arc lines", True)

        layers = []

        if show_bubbles:
            layers.append(pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color="[200, 30, 0, 140]",  # red semi-transparent
                get_radius="radius",
                pickable=True,
            ))

        if show_labels:
            layers.append(pdk.Layer(
                "TextLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_text="location",
                get_color=[0, 0, 0],
                get_size=12,
                get_alignment_baseline="'bottom'",
            ))

        if show_arcs:
            arc_data = pd.DataFrame([{
                "from_lon": 0,
                "from_lat": 0,
                "to_lon": row["longitude"],
                "to_lat": row["latitude"],
            } for _, row in df.iterrows()])

            layers.append(pdk.Layer(
                "ArcLayer",
                data=arc_data,
                get_source_position=["from_lon", "from_lat"],
                get_target_position=["to_lon", "to_lat"],
                get_source_color=[0, 0, 255, 120],   # blue
                get_target_color=[255, 0, 0, 160],   # red
                get_width=2,
                pickable=False,
            ))

        if layers:
            st.pydeck_chart(pdk.Deck(
                map_style="light",
                initial_view_state={
                    "latitude": 20,
                    "longitude": 0,
                    "zoom": 1.2,
                    "pitch": 30,
                },
                layers=layers,
                tooltip={"text": "{location}\nCases: {cases}"},
            ))
        else:
            st.error("Enable at least one layer to visualize data.")

except URLError as e:
    st.error(f"Connection error: {e.reason}")
