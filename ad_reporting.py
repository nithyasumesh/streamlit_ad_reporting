import streamlit as st

st.set_page_config(
    page_title="Fivetran Ad Reporting",
    layout="wide"
)

with open("README.md", "r") as f:
    readme_content = f.read()

st.markdown(readme_content)