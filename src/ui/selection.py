import streamlit as st
import os
import re

def render_selection():
    base_options = [
        d for d in os.listdir(".") 
        if os.path.isdir(d) and not d.startswith("OpenAI") and d != "src" and not d.startswith(".")
    ]
    openai_options = [
        d for d in os.listdir(".") 
        if os.path.isdir(d) and re.match(r"^OpenAI", d)
    ]

    col1, col2 = st.columns(2)

    with col1:
        base_folder = st.selectbox("Select your base folder:", base_options)
        st.session_state["base_folder"] = base_folder

    with col2:
        selected_data_folder = st.selectbox("Select your OpenAI data folder:", openai_options)
        st.session_state["selected_data_folder"] = selected_data_folder

    return base_folder
