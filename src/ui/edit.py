# edit.py
import streamlit as st
import os

def render_edit_tools():
    col1, col2 = st.columns([1, 1])

    # --- Create New Project Folder ---
    with col1:
        if st.button("➕ Create New Project"):
            st.session_state["show_create_input"] = True

        if st.session_state.get("show_create_input", False):
            new_folder = st.text_input("Enter new folder name:", key="new_folder_name")
            if st.button("Create Folder", key="create_folder_btn"):
                if new_folder and not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                    st.success(f"✅ Created folder: {new_folder}")
                    st.session_state["base_folder"] = new_folder
                    st.session_state["show_create_input"] = False
                elif os.path.exists(new_folder):
                    st.warning("⚠️ Folder already exists.")

    # --- Edit keywords.ssf File ---
# --- Edit keywords.ssf File ---
    with col2:
        if st.button("✏️ Edit Keywords"):
            st.session_state["show_keyword_editor"] = True

    if st.session_state.get("show_keyword_editor", False):
        folder = st.session_state.get("base_folder", "")
        if not folder:
            st.warning("⚠️ No base folder selected.")
        else:
            keywords_path = os.path.join(folder, "keywords.ssf")
            if os.path.exists(keywords_path):
                with open(keywords_path, "r", encoding="utf-8") as f:
                    current_keywords = f.read()
            else:
                current_keywords = ""

            with st.expander("📝 Editing keywords.ssf", expanded=True):
                updated_keywords = st.text_area("Edit keywords below:", value=current_keywords, height=200, key="keyword_editor")
                if st.button("💾 Save Keywords"):
                    with open(keywords_path, "w", encoding="utf-8") as f:
                        f.write(updated_keywords)
                    st.success("✅ Keywords updated successfully.")
                    st.session_state["show_keyword_editor"] = False
