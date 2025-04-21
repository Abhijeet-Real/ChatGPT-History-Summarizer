import json
import os
from collections import defaultdict

def load_keywords(base_path):
    """Load search keywords from a file in base_path."""
    filepath = os.path.join(base_path, "keywords.ssf")
    with open(filepath, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file if line.strip()]

def extract_messages_grouped(convo_json_path, keywords):
    """Extract, filter, and group relevant messages by conversation, sorted by time."""
    with open(convo_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    grouped_messages = defaultdict(list)
    convo_times = {}

    for convo in data:
        title = convo.get("title", "Untitled")
        convo_time = convo.get("create_time", "0")
        convo_times[title] = convo_time

        for message in convo.get("mapping", {}).values():
            msg_data = message.get("message")
            if not msg_data:
                continue

            content_dict = msg_data.get("content")
            if not content_dict:
                continue

            parts = content_dict.get("parts", [])
            if not parts or not isinstance(parts[0], (str, dict)):
                continue

            if isinstance(parts[0], str):
                content = parts[0].strip()
            elif isinstance(parts[0], dict):
                content = json.dumps(parts[0], ensure_ascii=False)
            else:
                continue

            if any(keyword in content.lower() for keyword in keywords):
                grouped_messages[title].append({
                    "date": convo.get("create_time", "0"),
                    "role": msg_data.get("author", {}).get("role", "unknown"),
                    "content": content
                })

    for msgs in grouped_messages.values():
        msgs.sort(key=lambda x: float(x["date"]))

    sorted_convos = dict(sorted(grouped_messages.items(), key=lambda kv: float(convo_times[kv[0]])))
    return sorted_convos

def save_grouped_results(grouped, output_path):
    """Save grouped relevant messages to 'extracted history.ssf'."""
    full_path = os.path.join(output_path, "extracted history.ssf")

    with open(full_path, "w", encoding="utf-8") as out_file:
        for title, messages in grouped.items():
            out_file.write(f"\n\n📌 Conversation: {title}\n" + "=" * (len(title) + 20) + "\n")
            for msg in messages:
                out_file.write(
                    f"[{msg['role'].upper()}] ({msg['date']}):\n{msg['content']}\n{'-'*50}\n"
                )

    print(f"✅ Extracted {len(grouped)} conversations to: {full_path}")
    return full_path

def main(base_folder, convo_json_path):
    keywords = load_keywords(base_folder)
    grouped = extract_messages_grouped(convo_json_path, keywords)
    save_grouped_results(grouped, base_folder)

if __name__ == "__main__":
    # Example usage:
    base = r"speech_to_speech"
    convo_json = r"OpenAI April 2025\conversations.json"  # relative to the Python file
    main(base, convo_json)
