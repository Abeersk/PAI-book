# RAG Knowledge Ingestion Pipeline

This repository contains an automated ingestion pipeline that extracts content from a deployed Docusaurus book, generates vector embeddings, and stores them in Qdrant for downstream RAG usage.

## Overview

The RAG (Retrieval-Augmented Generation) Knowledge Ingestion Pipeline is designed to:
- Fetch all valid content URLs from the deployed book's sitemap.xml
- Download and clean page HTML into readable text
- Chunk content into semantically meaningful segments
- Generate embeddings using Cohere Embed v3
- Store vectors and metadata in Qdrant Cloud (Free Tier)

## Features

- Automated sitemap parsing and URL extraction
- Clean HTML content extraction with removal of navigation elements
- Semantic text chunking for optimal embedding generation
- Cohere-powered vector embeddings
- Qdrant Cloud storage with metadata
- Comprehensive error handling and logging

## Prerequisites

- Python 3.11 or higher
- Pip package manager
- Git
- Qdrant Cloud account with API key
- Cohere API key

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd humanoid-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url
   BOOK_SITEMAP_URL=https://your-book-site.com/sitemap.xml
   ```

## Usage

Run the complete ingestion pipeline:
```bash
python scripts/run_ingestion_pipeline.py
```

For more options, run:
```bash
python scripts/run_ingestion_pipeline.py --help
```

## Project Structure

```
src/
├── rag_ingestion/
│   ├── __init__.py
│   ├── sitemap_fetcher.py      # Fetch and parse sitemap.xml
│   ├── content_extractor.py    # Extract text from HTML pages
│   ├── text_chunker.py         # Chunk text into semantic segments
│   ├── embedding_generator.py  # Generate embeddings using Cohere
│   ├── vector_storage.py       # Store vectors in Qdrant Cloud
│   ├── config.py               # Configuration management
│   └── main.py                 # Main pipeline orchestration
├── tests/
│   ├── unit/
│   └── integration/
└── scripts/
    └── run_ingestion_pipeline.py
```

## Configuration

The pipeline can be configured via environment variables in the `.env` file:

- `BOOK_SITEMAP_URL`: URL to the sitemap.xml of the target book
- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the collection to store vectors (default: "book_embeddings")
- `CHUNK_SIZE`: Maximum size of text chunks in characters (default: 2000)
- `CHUNK_OVERLAP`: Overlap between chunks in characters (default: 200)
- `BATCH_SIZE`: Number of items to process in each batch (default: 10)

## Testing

Run unit tests:
```bash
pytest tests/unit/
```

Run the complete pipeline test:
```bash
python -m pytest tests/unit/test_ingestion_pipeline.py
```

## Architecture

The pipeline consists of several interconnected modules:

1. **Sitemap Fetcher**: Retrieves and parses sitemap.xml to identify content URLs
2. **Content Extractor**: Downloads HTML pages and extracts clean text content
3. **Text Chunker**: Splits content into semantically meaningful segments
4. **Embedding Generator**: Creates vector embeddings using Cohere API
5. **Vector Storage**: Stores embeddings with metadata in Qdrant Cloud

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is part of the AI/Spec-Driven Book on Physical AI & Humanoid Robotics.