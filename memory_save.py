import os
import json
MEMORY_FILE = "chat_memory.json"

def load_messages() -> list[dict]:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list) and data:
                return data
        except:
            print("記憶檔案讀取失敗，將建立新的對話記錄。")

    return [{"role": "system", "content": "一律使用繁體中文回答。"}]


def save_messages(messages: list[dict]):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except:
        print(f"儲存記憶失敗")