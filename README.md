A simple Python-based local LLM chat application using Ollama.

This project demonstrates how to interact with a locally running large language model (LLM) via Ollama's HTTP API. It supports both single-turn text generation and multi-turn conversational interaction using the /api/generate and /api/chat endpoints.

The system also includes a basic Retrieval-Augmented Generation (RAG) pipeline, allowing it to search relevant document content and generate context-aware responses.

Features:
- Connects to a local Ollama server
- Supports both single-turn and multi-turn interactions
- Maintains conversation history as context
- Uses system prompts to control model behavior
- Saves chat history to a local file (JSON)
- Supports dual modes: chat mode and search mode
- Retrieves relevant document content using embeddings (RAG)
- Generates responses based on retrieved context

API Usage:
- /api/generate:
  Used for single-turn text generation. It takes a plain prompt as input and returns a one-time response without preserving conversation history.

- /api/chat:
  Used for multi-turn conversations. It stores previous messages, including system prompts, user inputs, and assistant responses, in a messages list. On each new turn, the full message history is sent back to the model to generate a context-aware reply.

Dual Modes:
- Chat Mode:
  A standard multi-turn conversation mode that maintains chat history and simulates memory by reusing previous messages as context.

- Search Mode:
  A retrieval-augmented mode that searches for relevant document chunks using embeddings, then sends the retrieved context along with the user query to the LLM to generate grounded answers.

Tech Stack:
- Python
- Requests
- Ollama (local LLM runtime)
- Chroma (vector database)
