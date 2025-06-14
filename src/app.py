# app.py
import streamlit as st
from ui.action_buttons import render_bottom
from ui.create_and_edit import render_edit_tools
from ui.progress_bar import render_live_data
from ui.select_folder import render_selection
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="ChatGPT History Summarizer", layout="wide", page_icon="🖋")
st.title("Project Summarization Dashboard")

# Auto-refresh every 10 seconds
st_autorefresh(interval=10 * 1000, key="refresh")

# Global state setup
def setup_state():
    if "progress" not in st.session_state:
        st.session_state["progress"] = (0, 1)
    if "summary_done" not in st.session_state:
        st.session_state["summary_done"] = True

setup_state()

render_edit_tools()

# Get folder path from selection section
base_folder = render_selection()

# Load data sections
if base_folder:
    render_live_data(base_folder)
    render_bottom(base_folder)
else:
    st.warning("🚫 Folder does not exist.")
