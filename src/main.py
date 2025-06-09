import History.history_pipeline as hp
import summary.summarize_chunks as sc
import summary.concat_summary as cs
import chunks.create_chunk as cc 

if __name__ == "__main__":
    folder = r"SIP"
    data_path_time = r"June 2025"
    data_path = r"OpenAI " + data_path_time + r"\conversations.json"
    model_name = "mistral"

    hp.history_pipeline(folder, data_path)
    cc.split_clean_file(folder, lines_per_chunk=1000, overlap_ratio=0.2)
    sc.summarize_all_chunks(folder, model_name)
    cs.concat_summaries(folder)