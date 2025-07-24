import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import requests
from urllib.error import URLError


@st.cache_data
def fetch_covid(radius):
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
    df["radius"] = np.log1p(df["cases"]) * 5000 * radius
    return df


try:
    radius = st.slider("Radius", 0.1, 2.0, 0.5)
    
    df = fetch_covid(radius)

    if df.empty:
        st.error("No data to display.")
    else:
        st.title("Global COVID Map via disease.sh API")
        sidebar = st.sidebar
        show = sidebar.checkbox("Show bubbles", True)
        show_lbl = sidebar.checkbox("Show country names", True)

        layers = []
        if show:
            layers.append(pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color="[200, 30, 0, 140]",
                get_radius="radius",
                pickable=True,
            ))
        if show_lbl:
            layers.append(pdk.Layer(
                "TextLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_text="location",
                get_color=[0, 0, 0],
                get_size=12,
                get_alignment_baseline="'bottom'",
            ))

        if layers:
            st.pydeck_chart(pdk.Deck(
                map_style="light",
                initial_view_state={"latitude": 20, "longitude": 0, "zoom": 1.2, "pitch": 20},
                layers=layers,
                tooltip={"text": "{location}\nCases: {cases}"},
            ))
        else:
            st.error("Enable at least one layer.")

except URLError as e:
    st.error(f"Connection error: {e.reason}")
