import history.extract_history as eh
import history.clean_history as ch
import summary.summarize_chunks as sc
import summary.concat_summary as cs
import chunks.create_chunk as cc
from utils.log_message import log_message 
import summary.rm_think as rt

if __name__ == "__main__":
    folder = r"Test"
    data_path_time = r"June 2025"
    data_path = r"OpenAI " + data_path_time + r"\conversations.json"
    model_name = "mistral"

    extacted_history_length = eh.main(folder, data_path)
    cleaned_history_length = ch.clean_project_log(folder)
    chunk_count = cc.split_clean_file(folder, lines_per_chunk=1000, overlap_ratio=0.2)
    sc.summarize_all_chunks(folder, model_name)
    rt.remove_think_blocks(base_folder)
    cs.concat_summaries(folder)
