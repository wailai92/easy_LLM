import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"

def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["response"]

def main():
    user_input = input("ask anything: ")
    try:
        reply = ask_llm(user_input)
        print("\nresponse: ")
        print(reply)
    except:
        print("ollama connection failed")

if __name__ == "__main__":
    main()