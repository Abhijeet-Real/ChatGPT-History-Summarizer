import os, time

def log_message(folder, message):
    log_path = os.path.join(folder, "log.ssf")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")