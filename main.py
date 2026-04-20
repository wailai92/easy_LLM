import memory_save
import requests

OLLAMA_URL_chat = "http://localhost:11434/api/chat"
OLLAMA_URL_generate = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"

def chat_llm(messages: list[dict]) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    response = requests.post(OLLAMA_URL_chat, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]

def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL_generate, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["response"]

def main():
    print("本地 LLM 聊天程式\n")
    print("輸入 exit 離開\n")

    messages = memory_save.load_messages()
    while True:
        user_input = input("ask anything: ").strip()
        if user_input == "exit":
            memory_save.save_messages(messages)
            break
        if not user_input:
            continue
        messages.append({
            "role": "user",
            "content": user_input
        })
        try:
            reply = chat_llm(messages)
            print(f"reply： {reply}\n")

            messages.append({
                "role": "assistant",
                "content": reply
            })
        except:
            print("ollama connection failed")

if __name__ == "__main__":
    main()