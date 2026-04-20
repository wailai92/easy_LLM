import memory_save
import requests
import chromadb
OLLAMA_URL_chat = "http://localhost:11434/api/chat"
OLLAMA_URL_generate = "http://localhost:11434/api/generate"
OLLAMA_URL_EMBED = "http://localhost:11434/api/embed"


MODEL_NAME = "gemma3:1b"
EMBED_MODEL = "embeddinggemma"
CHAT_MODE = ["RECORD", "SEARCH"]

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

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

def search_llm(question: str, contexts:list[str]) ->str:
    join_context = "\n\n".join(contexts)
    messages = [
        {
            "role": "system",
            "content": (
                "根據提供的文件內容回答。"
                "如果文件中沒有答案，就明確說不知道，不要亂猜。"
                "一律使用繁體中文回答。"
            )
        },
        {
            "role": "user",
            "content": f"文件內容：\n{join_context}\n\n問題：{question}"
        }
    ]
    response = requests.post(
        OLLAMA_URL_chat,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


def get_embedding(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_URL_EMBED,
        json={
            "model": EMBED_MODEL,
            "input": text
        },
        timeout=120
    )
    response.raise_for_status()
    data = response.json()
    return data["embeddings"][0]

def get_context(question, top_k = 3) -> list[str]:
    question_embed = get_embedding(question)
    results = collection.query(
        query_embeddings = [question_embed],
        n_results = top_k
    )
    try:
        return results["documents"][0]
    except:
        return []

def main():
    print("本地 LLM 聊天程式\n")
    print("輸入 exit 離開\n")
    print("搜尋更多指令輸入help(not done)\n")
    chat_mode = "RECORD"
    messages = memory_save.load_messages()
    while True:
        user_input = input("ask anything: ").strip()
        if user_input == "exit":
            memory_save.save_messages(messages)
            break
        elif user_input == "chmod s":
            chat_mode = "SEARCH"
            print("更改模式成SEARCH\n")
            continue
        elif user_input == "chmod r":
            chat_mode = "RECORD"
            print("更改模式成RECORD\n")
            continue
        elif not user_input:
            continue
        if chat_mode == "RECORD":
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
        elif chat_mode == "SEARCH":
            contexts = get_context(user_input)
            if not contexts:
                print("找不到相關資料\n")
                continue
            answer = search_llm(user_input, contexts)
            print("\n=== Retrieved Context ===")
            for i, ctx in enumerate(contexts, start=1):
                print(f"[{i}] {ctx}\n")
            print("=== Answer ===")
            print(f"{answer}\n")
            """
            先不加入
            messages.append({
                "role": "user",
                "content": user_input
            })
            messages.append({
                "role": "assistant",
                "content":answer
            })
            """

if __name__ == "__main__":
    main()