import streamlit as st
import history.extract_history as eh
import history.clean_history as ch
import summary.summarize_chunks as sc
import summary.concat_summary as cs
import chunks.create_chunk as cc
import threading
import os
import summary.rm_think as rt

def summarizer_thread(base_folder, model_name="mistral"):
    try:
        for done, total in sc.summarize_all_chunks(base_folder, model_name):
            st.session_state["progress"] = (done, total)       
    except Exception as e:
        pass
    finally:
        rt.remove_think_blocks(base_folder)
        cs.concat_summaries(base_folder)

def render_bottom(base_folder):
    from metadata.collector import collect_metadata
    meta = collect_metadata(base_folder)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Prepare Chunks"):
            data_path = os.path.join(st.session_state["selected_data_folder"], "conversations.json")
            extacted_history_length = eh.main(base_folder, data_path)
            cleaned_history_length = ch.clean_project_log(base_folder)
            chunk_count = cc.split_clean_file(base_folder, lines_per_chunk=250, overlap_ratio=0.2)
            st.success(f"✅ Prepared dataset with {chunk_count} chunks.")
    with col2:
        if st.button("Run Summarizer"):
            st.session_state["summary_done"] = False
            threading.Thread(target=summarizer_thread, args=(base_folder, "gemma3:4b"), daemon=True).start()