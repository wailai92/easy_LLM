A simple Python-based local LLM chat application using Ollama.

This project demonstrates how to interact with a locally running large language model (LLM) via Ollama's HTTP API. It explores both single-turn text generation and multi-turn conversational interaction by using the /api/generate and /api/chat endpoints.

Features:
- Connects to a local Ollama server
- Supports both single-turn and multi-turn interactions
- Maintains conversation history as context
- Uses system prompts to control model behavior
- Saves chat history to a local file (JSON)

API Usage:
- /api/generate:
  Used for single-turn text generation. It takes a plain prompt as input and returns a one-time response without preserving conversation history.

- /api/chat:
  Used for multi-turn conversations. It stores previous messages, including system prompts, user inputs, and assistant responses, in a messages list. On each new turn, the full message history is sent back to the model so it can generate a context-aware reply.

Tech Stack:
- Python
- Requests
- Ollama (local LLM runtime)
