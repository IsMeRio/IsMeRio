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

st.page_link("pages/bmi.py",label="BMI Calculate")
st.page_link("pages/command-prompts.py",label="command prompts")
st.page_link("pages/ai-caption.py",label="Ai image caption")
st.page_link("pages/XO.py",label="Ai Tic Tac Toe")
st.page_link("pages/Covid.py",label="Global COVID Map")
