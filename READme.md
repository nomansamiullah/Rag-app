# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with Flask, ChromaDB, and OpenAI.

## Features

- Document storage and retrieval using ChromaDB
- Conversational AI powered by OpenAI GPT
- RESTful API with comprehensive endpoints
- Modular architecture for easy maintenance
- Persistent conversation history

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env` file
4. Run the application: `python app.py`

## API Endpoints

- `POST /add_document` - Add single document
- `POST /add_documents` - Add multiple documents
- `POST /chat` - Chat with the bot
- `POST /retrieve` - Retrieve relevant documents
- `GET /health` - Health check
- `GET /collection_info` - Get collection information

## Environment Variables

```env
OPENAI_API_KEY=your-openai-api-key-here
CHROMA_DB_PATH=./data/chroma_db
COLLECTION_NAME=documents