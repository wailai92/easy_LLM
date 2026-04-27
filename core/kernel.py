import json
import core.memory_save as memory_save
from UI import main_page, search_page, setting_page
import requests
import chromadb
import sys 
import pygame

HELP_COMMANDS = {
    "exit": "離開程式",
    "chmod s": "切換到搜尋模式（RAG）",
    "chmod r": "切換到聊天模式",
    "help": "顯示所有指令",
    "rebuild": "db rebuild, 有新增新檔案時使用"
}

class Kernel():
    def __init__(self):
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        with open("UI/UI_config.json", "r", encoding="utf-8") as f:
            self.UI_config = json.load(f)
        self.messages = memory_save.load_messages()
        pygame.init()
        self.main = main_page.Main_page(self.UI_config)
        self.search = search_page.Search_page(self.UI_config)
        self.setting = setting_page.Setting_page(self.UI_config)
        self.current_page = self.main

    def pygame_run(self):
        self.screen_height = self.UI_config["scale"]["screen_height"]
        self.screen_width = self.UI_config["scale"]["screen_width"]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.current_page.handle_event(event)
            if self.current_page.next_page is not None:
                next_page = self.current_page.next_page
                self.current_page.next_page = None
                self.current_page = next_page
            self.current_page.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(144)
        


    def chat_llm(self) -> str:
        payload = {
            "model": self.config["model"]["chat_model_1"],
            "messages": self.messages,
            "stream": False
        }

        response = requests.post(self.config["server"]["chat_url"], json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()
        return data["message"]["content"]

    def ask_llm(self, prompt: str) -> str:
        payload = {
            "model": self.config["model"]["chat_model_1"],
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.config["server"]["generate_url"], json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()
        return data["response"]

    def search_llm(self, question: str, contexts:list[str]) ->str:
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
            self.config["server"]["chat_url"],
            json={
                "model": self.config["model"]["chat_model_1"],
                "messages": messages,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]


    def get_embedding(self, text: str) -> list[float]:
        response = requests.post(
            self.config["server"]["embed_url"],
            json={
                "model": self.config["model"]["embedding_model"],
                "input": text
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data["embeddings"][0]

    def get_context(self, question, top_k = 2):
        question_embed = self.get_embedding(question)
        collection = self.get_collection()
        results = collection.query(
            query_embeddings = [question_embed],
            n_results = top_k,
            include=["documents", "distances", "metadatas"]
        )
        try:
            return [results["documents"][0], results["metadatas"][0], results["distances"][0]]
        except:
            return []

    def get_collection(self):
        client = chromadb.PersistentClient(path=self.config["db_path"]["CHROMA_PATH"])
        return client.get_or_create_collection(name=self.config["db_path"]["COLLECTION_NAME"])