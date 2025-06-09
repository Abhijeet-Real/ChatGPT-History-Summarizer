import os, time
import re

from utils.log_message import log_message


def clean_project_log(base_folder):
    """Cleans extracted history and saves cleaned version in the same folder."""

    log_message(base_folder, "🧹 Step 2: Cleaning extracted messages...")

    input_path = os.path.join(base_folder, "extracted history.ssf")
    output_path = os.path.join(base_folder, "cleaned history.ssf")

    # If cleaned file already exists, do not re-clean
    if os.path.exists(output_path):
        log_message(base_folder, f" Cleaned file already exists at: {output_path}. Skipping cleaning.")
        return

    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Skip lines that look like code comments or workspace snippets
        if stripped.startswith("//") or stripped.startswith("#"):
            continue

        # Skip markdown heading or broken header blocks
        if re.match(r'^#+\s*\d*\.*\s*[\w\s]*$', stripped):
            continue

        # Skip structured junk like repeated variable patterns or placeholders
        if re.search(r"\$\{\d+:", stripped) or re.search(r"\$\d+", stripped):
            continue

        # Skip lines that are just too short to be meaningful
        if len(stripped) < 10:
            continue

        cleaned_lines.append(stripped)

    # Save cleaned version
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(cleaned_lines))

    log_message(base_folder, f"✅ Cleaned content saved to: {output_path} ({len(cleaned_lines)} useful lines kept)")

    return len(cleaned_lines)

if __name__ == "__main__":
    base_folder = r"speech_to_speech"  # ✅ Replace if needed
    clean_project_log(base_folder)
