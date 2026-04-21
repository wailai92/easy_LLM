A simple Python-based local LLM chat application using Ollama.

This project demonstrates how to interact with a locally running large language model (LLM) via Ollama's HTTP API. It supports both single-turn text generation and multi-turn conversational interaction using the /api/generate and /api/chat endpoints.

The system also implements a Retrieval-Augmented Generation (RAG) pipeline, enabling it to retrieve relevant document content from a local vector database and generate context-aware, grounded responses.

## Features
- Connects to a local Ollama server
- Supports both single-turn and multi-turn interactions
- Maintains conversation history as context (simulated memory)
- Uses system prompts to control model behavior
- Saves chat history to a local JSON file
- Supports dual modes: Chat Mode and Search Mode
- Implements embedding-based semantic search (RAG)
- Retrieves relevant document chunks from a vector database (Chroma)
- Applies distance-based filtering to ensure response reliability

## RAG Pipeline

The system follows a standard RAG workflow:

User Query
→ Embedding Generation
→ Vector Database Search (Chroma)
→ Top-k Retrieval
→ Context Filtering (based on similarity distance)
→ LLM Response Generation

## API Usage
- /api/generate:  Used for single-turn text generation. <br>
It takes a plain prompt as input and returns a one-time response without preserving conversation history.

- /api/chat:  Used for multi-turn conversations. <br>
It stores previous messages, including system prompts, user inputs, and assistant responses, in a messages list. On each new turn, the full message history is sent back to the model to generate a context-aware reply.

## Dual Modes:
- Chat Mode:  <br>
  A standard multi-turn conversation mode that maintains chat history and simulates memory using previous messages.

- Search Mode:  <br>
  A retrieval-augmented mode that:  
  - Converts user queries into embeddings
  - Retrieves the most relevant document chunks
  - Filters low-quality results using similarity distance
  - Injects high-quality context into the LLM to generate grounded answers

## Tech Stack:
- Python
- Requests
- Ollama (local LLM runtime)
- Chroma (vector database)


