import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center;'>IsMeRio Main Page</h1>", unsafe_allow_html=True)

st.page_link("pages/bmi.py",label="BMI Calculate",)