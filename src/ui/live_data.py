import streamlit as st
from metadata.collector import collect_metadata

def render_live_data(folder):

    st.divider()

    meta = collect_metadata(folder)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📦 Total Chunks", meta['Total Chunks'])
        avg_chunk_words = int(round(meta['Average Chunk Words'] / 500) * 500)
        st.write(f"Average Chunk Length: {avg_chunk_words} words")

    with col2:
        st.metric("🧾 Summarized Chunks", meta['Summarized Chunks'])
        avg_summary_words = int(round(meta['Average Summary Words'] / 50) * 50)
        st.write(f"Average Summary Length: {avg_summary_words} words")


    st.subheader("Progress")
    st.progress(meta['Progress %'] / 100)
