import streamlit as st
import history.extract_history as eh
import history.clean_history as ch
import summary.summarize_chunks as sc
import summary.concat_summary as cs
import chunks.create_chunk as cc
import threading
import os

def summarizer_thread(folder, model_name="mistral"):
    try:
        for done, total in sc.summarize_all_chunks(folder, model_name):
            st.session_state["progress"] = (done, total)       
    except Exception as e:
        pass
    finally:
        cs.concat_summaries(folder)

def render_bottom(folder):
    from metadata.collector import collect_metadata
    meta = collect_metadata(folder)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Prepare Chunks"):
            data_path = os.path.join(st.session_state["selected_data_folder"], "conversations.json")
            extacted_history_length = eh.main(folder, data_path)
            cleaned_history_length = ch.clean_project_log(folder)
            chunk_count = cc.split_clean_file(folder, lines_per_chunk=1000, overlap_ratio=0.2)
            st.success(f"✅ Prepared dataset with {chunk_count} chunks.")

    with col2:
        if st.button("🚀 Run Summarizer"):
            st.session_state["summary_done"] = False
            threading.Thread(target=summarizer_thread, args=(folder, "mistral"), daemon=True).start()
