import core.memory_save as memory_save
import core.build_index as build_index
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

HELP_COMMANDS = {
    "exit": "離開程式",
    "chmod s": "切換到搜尋模式（RAG）",
    "chmod r": "切換到聊天模式",
    "help": "顯示所有指令",
    "rebuild": "db rebuild, 有新增新檔案時使用"
}

def show_help():
    print("\n=== Available Commands ===\n")
    for cmd, desc in HELP_COMMANDS.items():
        print(f"{cmd:10} : {desc}")
    print()

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
                "你是一個文件問答助手。"
                "請只根據提供的文件內容回答問題。"
                "如果文件中有明確答案，請直接回答，不要說『我不知道』。"
                "只有在完全沒有相關資訊時，才回答『我不知道』。"
                "你必須一律使用繁體中文回答。"
                "如果文件內容是英文，請翻譯成繁體中文後再回答。"
            )
        },
        {
            "role": "user",
            "content": (
                f"文件內容：\n{join_context}\n\n"
                f"請根據以上內容，用繁體中文回答問題：{question}"
            )
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

def get_context(question, top_k = 2):
    question_embed = get_embedding(question)
    collection = get_collection()
    results = collection.query(
        query_embeddings = [question_embed],
        n_results = top_k,
        include=["documents", "distances", "metadatas"]
    )
    try:
        return [results["documents"][0], results["metadatas"][0], results["distances"][0]]
    except:
        return []

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)

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
        elif user_input == "rebuild":
            build_index.main()
            continue
        elif user_input == "help":
            show_help()
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
            results = get_context(user_input)
            docs = results[0]
            metas = results[1]
            dists = results[2]
            if not docs:
                print("找不到相關資料\n")
                continue
            
            #print(f"{dists[0]}, {dists[1]}\n")
            best = dists[0]
            if len(dists) > 1:
                second = dists[1]
                if best > 0.8 and (second - best) < 0.2:
                    print("結果不夠明確")
                    continue

            answer = search_llm(user_input, docs)
            print("\n=== Retrieved Context ===")
            for i, (doc, meta) in enumerate(zip(docs, metas), 1):
                print(f"[{i}] ({meta['source']}) {doc}\n")
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